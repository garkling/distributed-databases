import os
import json
from pprint import pprint
from random import randrange
from datetime import timedelta, datetime, date

from dotenv import load_dotenv
from pymongo import MongoClient

from query import Query, UpdateQuery

load_dotenv()
db = os.environ["MONGO_DATABASE"]
host = os.environ["MONGO_HOST"]
port = int(os.environ["MONGO_PORT"])
user = os.environ["MONGO_DB_USER"]
password = os.environ["MONGO_DB_PASSWORD"]


class MongoCollection:

    def __init__(self, collection, **create_args):
        self.client = MongoClient(host=host, port=port, username=user, password=password, authSource=db)
        self.db = self.client.get_database(db)
        self.collection = self.db.create_collection(collection, **create_args) if create_args else self.db.get_collection(collection)

    def insert_many(self, filename) -> bool:
        with open(filename) as file:
            data = json.load(file)

        return self.collection.insert_many(data).acknowledged

    def insert(self, doc: dict, auto_create_date=True):
        if auto_create_date:
            create_date = datetime.now().replace(microsecond=0)
            doc['create_date'] = create_date

        return self.collection.insert_one(doc).inserted_id

    def find(self, query, projection=None):
        fields, query_obj = Query.evaluate(query)

        if projection == 'all': projection = None
        else:
            projection = list(map(str.strip, projection.split(","))) if projection else fields

        query_obj = query_obj.project(projection)

        with self.collection.aggregate(query_obj.stages) as cur:
            return list(cur)

    def update(self, query, update_query):

        found = self.find(query, projection='_id')
        matches = [o['_id'] for o in found]

        _, query_obj = Query.evaluate(f"_id.in_(*{matches})")
        fields, update_query_obj = UpdateQuery.evaluate(update_query, outer_ctx=found[0] if found else None)

        updated = self.collection.update_many(query_obj.query, update_query_obj.query)

        return updated, self.find(query, projection='all')

    def remove(self, query):
        found = self.find(query, projection='_id')
        matches = [o['_id'] for o in found]

        _, query_obj = Query.evaluate(f"_id.in_(*{matches})")

        updated = self.collection.delete_many(query_obj.query)

        return updated, self.find(query, projection='all')

    def drop(self):
        self.db.drop_collection(self.collection)

    @staticmethod
    def apply(self, op, *args, **kwargs):
        op = self.ops[op]
        return op(self, *args, **kwargs)

    def info(self):
        return self.collection.full_name, self.collection.options()

    @staticmethod
    def _populate(cls=None):
        cls = cls or MongoCollection
        items = cls('items')
        orders = cls('orders')

        customers = {
            (1, "Jessica", "Anderson"): (
            "123 Main St, Anytown, USA, 54321", "(category == 'Laptops') & (model == 'UltraBook X1')"),
            (2, "Jessica", "Anderson"): (
            "123 Main St, Anytown, USA, 54321", "(category == 'TV') & (price <= 600.00)"),
            (1, "Michael", "Brown"): (
            "101 Pine St, Nowhereville, USA, 13579", "(brand == 'Apple') | (brand == 'TechVision')"),
            (2, "Michael", "Brown"): (
            "101 Pine St, Nowhereville, USA, 13579", "(category == 'Smart Watch') & (water_resistance == '30 meters')"),
            (1, "Christopher", "Martinez"): (
            "8 Abbey Road, Manchester, UK, M1 1AA", "(category == 'TV') & resolution.in_('4K UHD', 'FUll HD')"),
            (1, "Ashley", "Durden"): (
            "10 Unter den Linden, Berlin, Germany", "(model == 'GamerPro 2000') | (storage == '512GB SSD')"),
            (2, "Ashley", "Durden"): (
            "10 Unter den Linden, Berlin, Germany", "model == 'iPhone 13'"),
        }

        assert items.insert_many('items.json'), 'Failed to populate the `items` collection'

        for (_, *name), (address, order_query) in customers.items():
            ordered_items = items.find(order_query, projection='all')

            inserted = orders.insert({
                "order_number": randrange(10000, 50000),
                "date": (date(2024, 1, 1) + timedelta(randrange(1, 365))).isoformat(),
                "total_sum": sum(i['price'] for i in ordered_items),
                "customer": {
                    "name": name[0],
                    "surname": name[1],
                    "phones": [randrange(10 ** 6, 10 ** 7 - 1) for _ in range(randrange(1, 3))],
                    "address": address
                },
                "payment": {
                    "card_owner": name,
                    "cardId": randrange(10 ** 15, 10 ** 16 - 1)
                },
                "items_id": [i['_id'] for i in ordered_items]
            }, auto_create_date=False)

            print(inserted)

        return True

    ops = dict()


MongoCollection.ops.update({
    "insert_many": MongoCollection.insert_many,
    "insert": MongoCollection.insert,
    "get": MongoCollection.find,
    "update": MongoCollection.update,
    "remove": MongoCollection.remove,
    "populate": MongoCollection._populate,
    "drop": MongoCollection.drop,
})


prompts = {
    "get"   : lambda: {"query": input('Query: '), "projection": input("Fields to show ([query fields] is default): ")},
    "update": lambda: {"query": input('Query [empty query updates all!!]: '), "update_query": input("Update query: ")},
    "remove": lambda: {"query": input('Query [empty query removes all!!]: ')},
    "insert": lambda: {"doc": json.loads(input('Document to insert: '))}
}


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='MongoDB client wrapper using Python operators and methods')
    parser.add_argument('operation', choices=MongoCollection.ops, type=str, help="CRUD operation")
    parser.add_argument('collection', type=str, nargs='?', help="MongoDB collection name")

    parser.add_argument('--params', nargs="+", metavar='KEY=VALUE', help="parameters to create MongoDB collection")
    parser.add_argument('--filename', type=str, default=argparse.SUPPRESS, help="filename for `insert_many` operation")
    exclude = ("operation", "collection", "params")

    args = parser.parse_args()

    assert not (args.operation == "insert_many" and 'filename' not in args), parser.error(f"`{args.operation}` action requires a --filename argument")
    assert not (args.operation != "populate" and args.collection is None), parser.error(f"`{args.operation}` action requires a `collection` positional")

    create_params = {}
    if args.params is not None:
        try:
            assert not any(';' in p for p in args.params)
            create_params = {
                k.strip(): eval(v)
                for k, v in map(lambda p: p.split('='), args.params)
            } if args.params else {}
        except Exception:
            parser.error(f"Invalid collection create parameters")

    collection = MongoCollection(args.collection, **create_params) if args.collection else MongoCollection

    prompt = prompts.get(args.operation, lambda *_: {})
    cmd_kwargs = vars(args)
    kw = {**prompt(), **{k: cmd_kwargs[k] for k in set(cmd_kwargs).difference(exclude)}}

    res = MongoCollection.apply(collection, args.operation, **kw)
    pprint(res)
