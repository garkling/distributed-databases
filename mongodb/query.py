import re
from typing import Iterable
from bson import ObjectId


class Query:

    def __init__(self, name, query = None, stages = None):
        self.field = name
        self._query = query or dict()
        self._stages = stages or dict()

    def __eq__(self, other):
        query = {self.field: other}
        return self.__class__(self.field, query)

    def __ne__(self, other):
        query = {self.field: {"$ne": other}}
        return self.__class__(self.field, query)

    def __lt__(self, other):
        query = {self.field: {"$lt": other}}
        return self.__class__(self.field, query)

    def __gt__(self, other):
        query = {self.field: {"$gt": other}}
        return self.__class__(self.field, query)

    def __ge__(self, other):
        query = {self.field: {"$gte": other}}
        return self.__class__(self.field, query)

    def __le__(self, other):
        query = {self.field: {"$lte": other}}
        return self.__class__(self.field, query)

    def __or__(self, other: 'Query'):
        query = {"$or": [
            *self.query.get('$or', [self.query]),
            *other.query.get('$or', [other.query])
        ]}
        # common = dict(map(lambda k: (k, {"$in": [self.query[k], other.query[k]]}), set(self.query).intersection(other.query)))

        return self.__class__(self.field, query)

    def __and__(self, other: 'Query'):
        # common = set(self.query).intersection(other.query)
        # assert not common or common.issubset(('$or', '$and'))

        query = {"$and": [
            *self.query.get('$and', [self.query]),
            *other.query.get('$and', [other.query])
        ]}
        return self.__class__(self.field, query)

    def __getitem__(self, item):
        field = f'{self.field}.{item}'
        return self.__class__(field, self.query)

    def join(self, from_, where=None, on=None, alias="joined"):
        _, result = ExpressionQuery.evaluate(where)

        local_field = on or self.field
        foreign_collection, foreign_field = from_.split('.')
        stages = {
            "$lookup": {
                "from": foreign_collection,
                "localField": local_field,
                "foreignField": foreign_field,
                "pipeline": [{"$match": result.query}] if result.query else [],
                "as": alias
            },
            "$match": {alias: {"$ne": []}},
            "$project": {alias: 1}
        }

        return self.__class__(self.field, self.query, stages)

    def project(self, fields):
        projections = self._stages.pop('$project', {})

        stages = self._stages
        if fields is not None:
            collisions = set(f.split('.')[0] for f in fields)
            projections = {
                key: projections[key] for key in filter(lambda k: k not in collisions, projections.keys())
            }
            stages = {
                **self._stages,
                "$project": {**projections, **dict.fromkeys(fields, 1)}

            }

        return self.__class__(self.field, self.query, stages)

    def distinct(self, *by):
        _id = ["$"+f for f in by] or "$" + (self.field if not self._query else '_id')

        groups = self._stages.get('$group', [])
        stages = {
            **self._stages,
            "$group": [
                *groups,
                {"_id": _id},
            ],
            "$project": {
                "field": "$_id",
                "_id": 0
            }
        }

        return self.__class__(self.field, self.query, stages)

    def count(self, by=None):
        _id = "$" + (by or (self.field if not self._query else '_id'))
        groups = self._stages.get('$group', [{"_id": _id}])
        stages = {
            **self._stages,
            "$group": [
                *groups,
                {"_id": None, "count": {"$sum": {
                    "$cond": {
                        "if": {"$isArray": "$_id"},
                        "then": {"$size": "$_id"},
                        "else": 1
                    }
                }}}
            ],
            "$project": {
                "_id": 0,
                "count": 1
            }
        }

        return self.__class__(self.field, self.query, stages)

    def in_(self, *coll: Iterable):
        query = {self.field: {"$in": list(coll)}}
        return self.__class__(self.field, query)

    def nin(self, *coll: Iterable):
        query = {self.field: {"$nin": list(coll)}}
        return self.__class__(self.field, query)

    def exists(self):
        query = {self.field: {"$exists": True}}
        return self.__class__(self.field, query)

    def not_exists(self):
        query = {self.field: {"$exists": False}}
        return self.__class__(self.field, query)

    def between(self, left, right):
        query = {self.field: {"$gt": left, "$lt": right}}
        return self.__class__(self.field, query)

    def __getattr__(self, item):
        return self.__class__(self.field + '.' + item, self.query)

    def __repr__(self):
        return str(self.query)

    def __str__(self):
        return str(self.query)

    @property
    def query(self):
        return self._query

    @property
    def stages(self):
        stages = self._stages.items()
        stages = [
            *[{k: i} for (k, v) in stages for i in v if isinstance(v, list)],
            *[{k: s} for (k, s) in stages if not isinstance(s, list)]
        ]

        stages = [{"$match": self._query}] + stages
        return stages

    @classmethod
    def evaluate(cls, query, outer_ctx=None):
        if not query: return None, cls('')
        try:
            outer_ctx = dict(null=None, ObjectId=ObjectId, **outer_ctx or {})
            ctx = {
                f: cls(f) for f in map(
                    lambda expr: re.match(r'\(*([a-z_]+)\s?', expr, flags=re.IGNORECASE).group(1),
                    re.split(r'[|&]\s?', query, flags=re.IGNORECASE)
                )
            }

            return list(ctx.keys()), eval(query, outer_ctx, ctx)
        except Exception as e:
            print(f'Invalid query - {e}')
            raise

    __add__ = __sub__ = __mul__ = lambda *_: exec('raise(NotImplementedError("Operation is not supported"))')


class UpdateQuery(Query):

    def __eq__(self, other):
        set_ = self._query.get("$set", {})
        query = {
            **self._query,
            "$set": {**set_, self.field: other}
        }

        return self.__class__(self.field, query)

    def unset(self):
        unset_ = self._query.get("$unset", {})
        query = {
            **self._query,
            "$unset": {**unset_, self.field: ""}
        }

        return self.__class__(self.field, query)

    def __add__(self, other):
        operator, subquery = ("$inc", {self.field: other})
        if isinstance(other, Iterable):
            operator, subquery = ("$push", {self.field: {"$each": list(other)}})

        present = self._query.get(operator, {})
        query = {
            **self._query,
            operator: {**present, **subquery}
        }

        return self.__class__(self.field, query)

    def __sub__(self, other):
        operator, subquery = ("$inc", {self.field: other})
        if isinstance(other, Iterable):
            operator, subquery = ("$pull", {self.field: {"$in": list(other)}})

        present = self._query.get(operator, {})
        query = {
            **self._query,
            operator: {**present, **subquery}
        }

        return self.__class__(self.field, query)

    def __mul__(self, other):
        mul = self._query.get("$mul", {})
        query = {
            **self._query,
            "$mul": {**mul, **{self.field: other}}
        }

        return self.__class__(self.field, query)

    def __and__(self, other):
        common = {k : {**self._query[k], **other._query[k]} for k in set(self._query).intersection(other._query)}

        query = {**self._query, **other._query, **common}
        return self.__class__(self.field, query)

    @property
    def stages(self):
        return [self.query]

    __or__ = __lt__ = __gt__ = __le__ = __ge__ = lambda *_: exec('raise(NotImplementedError("Operation is not supported"))')


class ExpressionQuery(Query):

    def __init__(self, field, query = None):
        super().__init__(field, query)
        self.field = '$' + self.field

    def __eq__(self, other):
        query = {"$eq": [other, self.field]}
        return self.__class__(self.field, query)

    def __ne__(self, other):
        query = {"$ne": [other, self.field]}
        return self.__class__(self.field, query)

    def __lt__(self, other):
        query = {"$lt": [other, self.field]}
        return self.__class__(self.field, query)

    def __le__(self, other):
        query = {"$lte": [other, self.field]}
        return self.__class__(self.field, query)

    def __gt__(self, other):
        query = {"$gt": [other, self.field]}
        return self.__class__(self.field, query)

    def __ge__(self, other):
        query = {"$gte": [other, self.field]}
        return self.__class__(self.field, query)

    def in_(self, *coll: Iterable):
        query = {{"$in": [list(coll), self.field]}}
        return self.__class__(self.field, query)

    def nin(self, *coll: Iterable):
        query = {{"$nin": [list(coll), self.field]}}
        return self.__class__(self.field, query)

    @property
    def query(self):
        return {"$expr": self._query}
