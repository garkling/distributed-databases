import json
from uuid import uuid4
from datetime import datetime

from cassandra import cluster


def on_request(rf: cluster.ResponseFuture):
    if not isinstance(rf.query, cluster.BatchStatement):
        print(f"\nExecuting \n\t{rf.message.query}")


class Store:

    def __init__(self, seeds, port, keyspace, exec_profiles: dict):
        self.cluster = cluster.Cluster(
            contact_points=seeds,
            port=int(port),
            execution_profiles=exec_profiles,
            protocol_version=cluster.ProtocolVersion.V5
        )
        self.keyspace = keyspace

    def execute(self, query, data=None, exec_profile = cluster.EXEC_PROFILE_DEFAULT):
        with self.cluster.connect(self.keyspace) as session:
            session.add_request_init_listener(on_request)
            res = session.execute(query, data, execution_profile=exec_profile)

            return res

    def batch_insert_items(self, data):
        """Batch insert, but only for a single partition at once"""
        query = """INSERT INTO items (category, brand, model, price, props, id) VALUES (%s, %s, %s, %s, %s, %s) IF NOT EXISTS"""
        batch = cluster.BatchStatement(consistency_level=cluster.ConsistencyLevel.LOCAL_QUORUM)
        for entry in data: batch.add(query, (*entry, uuid4()))

        return self.execute(batch)

    def batch_insert_orders(self, data):
        """Batch insert, but only for a single partition at once"""
        query = """INSERT INTO orders (customer_name, order_date, items, order_total, id) VALUES (%s, %s, %s, %s, %s) IF NOT EXISTS"""
        batch = cluster.BatchStatement(consistency_level=cluster.ConsistencyLevel.LOCAL_QUORUM)
        for entry in data: batch.add(query, (*entry, uuid4()))

        return self.execute(batch)

    def get_categories(self):
        return self.execute(
            """SELECT DISTINCT category FROM items"""
        ).all()

    def get_item(self, category, brand, model):
        return self.execute(
            """SELECT * FROM items WHERE category = %s AND brand = %s AND model = %s""",
            (category, brand, model)
        ).one()

    def get_items_sorted_by_price(self, category):
        return self.execute(
            """SELECT * FROM items_by_price WHERE category = %s""",
            (category, )
        ).all()

    def get_item_by_id(self, uuid):
        return self.execute(
            """SELECT category, brand, model, price, props FROM items_by_id WHERE id = %s""",
            (uuid,)
        ).one()

    def get_items_by_model(self, category, model):
        return self.execute(
            """SELECT * FROM items WHERE category = %s AND model LIKE %s""",
            (category, f'%{model}%')
        ).all()

    def get_items_by_price_range(self, category, from_, to_):
        return self.execute(
            """SELECT * FROM items_by_price WHERE category = %s AND price >= %s AND price <= %s""",
            (category, from_, to_)
        ).all()

    def get_items_by_price_by_brand(self, category, price, brand):
        return self.execute(
            """SELECT * FROM items_by_price WHERE category = %s AND price = %s AND brand = %s""",
            (category, price, brand)
        ).all()

    def get_items_by_property(self, p_key, p_value=None, category=None):
        params = ()
        query = """SELECT * FROM items WHERE"""
        if category is not None:
            query += """ category = %s AND"""
            params += (category, )

        if p_value is not None:
            query += """ props[%s] = %s"""
            params += (p_key, p_value, )
        else:
            query += """ props CONTAINS KEY %s"""
            params += (p_key, )

        return self.execute(query, params).all()

    def update_or_insert_item_property(self, category, brand, model, p_key, p_value):
        self.execute(
            """UPDATE items 
            SET props = props + {%s: %s} 
            WHERE category = %s AND brand = %s AND model = %s""",
            (p_key, p_value, category, brand, model)
        )
        return True

    def update_or_insert_item_property_by_id(self, uuid, p_key, p_value):
        item = self.get_item_by_id(uuid)

        if item is not None:
            return self.update_or_insert_item_property(item['category'], item['brand'], item['model'], p_key, p_value)

    def delete_item_property(self, category, brand, model, p_key):
        self.execute(
            """UPDATE items 
            SET props = props - {%s} 
            WHERE category = %s AND brand = %s AND model = %s""",
            (p_key, category, brand, model)
        )
        return True

    def delete_item_property_by_id(self, uuid, p_key):
        item = self.get_item_by_id(uuid)

        if item is not None:
            return self.delete_item_property(item['category'], item['brand'], item['model'], p_key)

    def insert_order(self, *params, ttl: int = None):
        query = """INSERT INTO orders (customer_name, order_date, items, order_total, id) VALUES (%s, %s, %s, %s, %s) IF NOT EXISTS"""
        params = (*params, uuid4())

        if ttl is not None:
            query += """ USING TTL %s"""
            params += (int(ttl), )

        return self.execute(query, params).was_applied

    def insert_order_json(self, body: str, ttl: int = None):
        query = """INSERT INTO orders JSON %s IF NOT EXISTS"""
        params = (
            json.dumps({**json.loads(body), "id": str(uuid4())}),
        )

        if ttl is not None:
            params += int(ttl)
            query += """ USING ttl %s"""

        return self.execute(query, params).was_applied

    def get_order(self, customer_name, order_date):
        return self.execute(
            """SELECT * FROM orders WHERE customer_name = %s AND order_date = %s""",
            (customer_name, order_date)
        ).one()

    def get_orders_in_json(self, customer_name):
        return self.execute(
            """SELECT JSON * FROM orders WHERE customer_name = %s""",
            (customer_name, )
        ).all()

    def get_order_customers(self):
        return self.execute(
            """SELECT DISTINCT customer_name FROM orders"""
        ).all()

    def get_orders(self, customer_name):
        return self.execute(
            """SELECT * FROM orders WHERE customer_name = %s""",
            (customer_name, )
        ).all()

    def get_orders_by_item_id(self, customer_name, uuid):
        return self.execute(
            """SELECT * FROM orders WHERE customer_name = %s AND items CONTAINS %s""",
            (customer_name, uuid)
        ).all()

    def get_orders_by_date_range(self, customer_name, from_, to_):
        return self.execute(
            """SELECT order_date, order_total, items FROM orders 
            WHERE customer_name = %s AND order_date >= %s AND order_date <= %s""",
            (customer_name, from_, to_)

        ).all()

    def get_order_count_by_date_range(self, customer_name, from_, to_):
        return self.execute(
            """SELECT COUNT(id) AS count FROM orders 
            WHERE customer_name = %s AND order_date >= %s AND order_date <= %s""",
            (customer_name, from_, to_)

        ).one()

    def get_order_total(self, customer_name, order_date):
        return self.execute(
            """SELECT order_total FROM orders WHERE customer_name = %s AND order_date = %s""",
            (customer_name, order_date)
        ).one()

    def get_orders_total_sum_by_customers(self):
        return self.execute(
            """SELECT customer_name, SUM(order_total) AS total_total FROM orders
            GROUP BY customer_name""",
        ).all()

    def get_max_order_total_by_customers(self):
        return self.execute(
            """SELECT customer_name, MAX(order_total) AS max_total, order_date, items FROM orders
            GROUP BY customer_name""",
        ).all()

    def __prepare_order_items_update(self, items_id: set):
        total_diff = 0
        items = set()
        for uuid in items_id:
            item = self.get_item_by_id(uuid)
            if item is not None:
                items = {*items, uuid}
                total_diff += item['price']

        return items, total_diff

    def insert_order_items(self, customer_name, order_date, items):
        items, total_diff = self.__prepare_order_items_update(items)

        applied = False
        while not applied:
            current_total = self.get_order_total(customer_name, order_date)
            current_total = current_total['order_total'] if current_total else 0

            applied = self.execute(
                """UPDATE orders 
                SET items = items + %s, order_total = %s
                WHERE customer_name = %s AND order_date = %s
                IF order_total = %s""",
                (items, current_total + total_diff, customer_name, order_date, current_total)
            ).was_applied

        return applied

    def delete_order_items(self, customer_name, order_date, items):
        items, total_diff = self.__prepare_order_items_update(items)

        applied = False
        while not applied:
            current_total = self.get_order_total(customer_name, order_date)
            current_total = current_total['order_total'] if current_total else 0

            applied = self.execute(
                """UPDATE orders 
                SET items = items - %s, order_total = %s
                WHERE customer_name = %s AND order_date = %s
                IF order_total = %s""",
                (items, current_total - total_diff, customer_name, order_date, current_total)
            ).was_applied

        return applied

    def get_order_total_writetime(self):
        data = self.execute(
            """SELECT id, order_date, WRITETIME(order_total) AS write_time FROM orders"""
        ).all()

        return [
            {**row, "write_time": datetime.fromtimestamp(row['write_time'] / 1_000_000).isoformat()}
            for row in data
        ]

    def close(self):
        self.cluster.shutdown()
