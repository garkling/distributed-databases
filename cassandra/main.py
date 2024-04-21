import os
import sys
import json
import uuid
from pprint import pformat
from itertools import chain
from textwrap import indent
from random import randrange as rng
from time import sleep

from cassandra import cluster
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra.query import dict_factory, tuple_factory
from dotenv import load_dotenv

from store import Store
from orders import customer_orders
sys.path.append('..')
from logger import get_logger


load_dotenv()
TAB = '\t'
SEED_NODE, PORT = os.environ['CASSANDRA_CLUSTER_SEED_NODE'].split(":")
KEYSPACE = os.environ['CASSANDRA_KEYSPACE']
EXEC_PROFILES = {
    cluster.EXEC_PROFILE_DEFAULT: cluster.ExecutionProfile(
        load_balancing_policy=DCAwareRoundRobinPolicy("datacenter1"),
        consistency_level=cluster.ConsistencyLevel.LOCAL_QUORUM,
        row_factory=dict_factory
    ),
    "tuple_format": cluster.ExecutionProfile(
        load_balancing_policy=DCAwareRoundRobinPolicy("datacenter1"),
        consistency_level=cluster.ConsistencyLevel.LOCAL_QUORUM,
        row_factory=tuple_factory
    )
}

logger = get_logger("cassandra")


def populate_items(filename):
    with open(filename) as datafile:
        data = json.load(datafile)
        by_category = {}
        for item in data:
            by_category.setdefault(item["category"], []).append(item.values())

    for category, items in by_category.items():
        res = store.batch_insert_items(items)
        print(f"Inserted {len(items)} items in category {category}; [applied] - {res.was_applied}")


def populate_orders():
    for customer, items_selected in customer_orders.items():
        orders = tuple()
        for date, queries in items_selected.items():
            ids = set()
            total = 0
            for query in queries:
                query, client_filter = query if isinstance(query, tuple) else (query, None)
                items = store.execute(query).all()
                if client_filter:
                    *keys, value = client_filter
                    nested_keys = len(keys) == 2
                    items = list(filter(lambda item: (item[keys[0]][keys[1]] if nested_keys else item[keys[0]]) == value, items))

                total += sum(item['price'] for item in items)
                ids = {*ids, *set(item['id'] for item in items)}

            orders += ((customer, date, ids, total), )

        res = store.batch_insert_orders(orders)
        print(f"\nInserted {len(orders)} orders by customer {customer}; [applied] - {res.was_applied}")


actions = {
    'populate'          : lambda: (populate_items("items.json"), populate_orders()),
    'truncate'          : lambda: (store.execute("TRUNCATE items"), store.execute("TRUNCATE orders")),
    'run_items_tasks'   : lambda: __run_interactive_mode(item_tasks),
    'run_orders_tasks'  : lambda: __run_interactive_mode(order_tasks)
}

item_tasks = {
    "0" : (lambda: store.get_categories(), ),
    "1" : (lambda: store.execute("DESCRIBE TABLE items").one(), ),
    "2" : (lambda: store.get_items_sorted_by_price("Laptops"), ),
    "3a": (lambda: store.get_items_by_model("Smartphones", "Ultra"), ),
    "3b": (lambda: store.get_items_by_price_range("TV", 1000, 2000), ),
    "3c": (lambda: store.get_items_by_price_by_brand("Laptops", 1299.99, "Dell"), ),
    "4a": (lambda: store.get_items_by_property("fast_charge", category="Smartphones"), ),
    "4b": (lambda: store.get_items_by_property("screen_matrix", category="Laptops", p_value= "IPS"), ),
    "5a": (lambda: store.update_or_insert_item_property("Smartphones", "Huawei", "Huawei Mate 40 Pro", "color", "Mystery Silver"),
           lambda: store.get_item("Smartphones", "Huawei", "Huawei Mate 40 Pro")),  # check

    "5b": (lambda: store.update_or_insert_item_property("Tablets", "Apple", "iPad Pro (12.9-inch, 5th Gen)", "stylus", "Apple Pencil"),
           lambda: store.get_item("Tablets", "Apple", "iPad Pro (12.9-inch, 5th Gen)")),    # check

    "5c": (lambda: store.delete_item_property("Laptops", "HP", "HP Envy 15", "os"),
           lambda: store.get_item("Laptops", "HP", "HP Envy 15"))   # check
}
order_tasks = {
    "0" : (lambda: store.get_order_customers(), ),
    "1" : (lambda: store.execute("DESCRIBE TABLE orders").one(), ),
    "2" : (lambda: store.get_orders("James Cooper"), ),
    "3" : (lambda: store.get_orders_by_item_id('Liam Harris', __get_customer_random_items('Liam Harris')), ),
    "4" : (lambda: store.get_orders_by_date_range('Liam Harris', "2024-01-01 00:00:00", "2024-12-31 00:00:00"), ),
    "5" : (lambda: store.get_orders_total_sum_by_customers(), ),
    "6" : (lambda: store.get_max_order_total_by_customers(), ),
    "7a": (lambda: store.insert_order_items('Sophia Martin', '2024-04-01 15:11:39', __get_random_items(count=3)),
           lambda: store.get_order("Sophia Martin", "2024-04-01 15:11:39")),    # check

    "7b": (lambda: store.delete_order_items('Ava Turner', '2023-11-11 19:44:12', __get_customer_random_items('Ava Turner', '2023-11-11 19:44:12', count=2)),
           lambda: store.get_order("Ava Turner", "2023-11-11 19:44:12")),   # check
    "8" : (lambda: store.get_order_total_writetime(), ),
    "9" : (lambda: store.insert_order("Mike Smith", "2024-04-15 22:59:59", *__get_random_items_with_total_price(count=2), ttl=5),
           lambda: store.get_order("Mike Smith", "2024-04-15 22:59:59"),    # check
           lambda: (print(f"\nSleeping for 5 seconds, sleep(5) function will return None"), sleep(5)),   # check
           lambda: store.get_order("Mike Smith", "2024-04-15 22:59:59")),   # check

    "10": (lambda: store.get_orders_in_json("Mia Rodriguez"), ),
    "11": (lambda: store.insert_order_json(
                                        json.dumps({
                                            "customer_name": "Noah Young",
                                            "order_date": "2023-12-21 14:22:17",
                                            **dict(zip(("items", "order_total"), __get_random_items_with_total_price(count=3)))
                                        }, default=lambda obj: list(obj) if isinstance(obj, set) else str(obj))
                                        ),
           lambda: store.get_order("Noah Young", "2023-12-21 14:22:17")),
}


# helpers
def __get_customer_random_items(customer_name, order_date=None, count=1):
    params = (customer_name, )
    query = """SELECT items FROM orders WHERE customer_name = %s"""
    if order_date is not None:
        query += """ AND order_date = %s"""
        params += (order_date, )

    items = store.execute(query, params, exec_profile="tuple_format").all()
    items = tuple(filter(None, chain(*chain(*items))))
    print(f"Result\n{indent(pformat(items), TAB)}")

    selected = tuple(items[rng(0, len(items))] if items else uuid.uuid4() for _ in range(count))
    return set(selected) if count > 1 else selected[0]


def __get_random_items(count=1):
    items = tuple(
        row[0] for row in store.execute("SELECT id FROM items", exec_profile="tuple_format").all()
    )

    if items:
        return set(items[rng(0, len(items))] for _ in range(count))

    return set()


def __get_random_items_with_total_price(count=1):
    items = tuple(
        row for row in store.execute("SELECT id, price FROM items", exec_profile="tuple_format").all()
    )

    if items:
        selected = set(items[rng(0, len(items))] for _ in range(count))
        return set(item[0] for item in selected), sum(item[1] for item in selected)

    return set(), 0


def __run_interactive_mode(tasks):
    print(f"Available tasks: {tuple(tasks)}")
    while True:
        try:
            key = input("Enter the task number [leave empty to exit]: ")
            if not key: break
            assert key in tasks

            print(f"{key:-^100}")
            task, *checks, = tasks[key]
            res = task()
            print(f"Result\n{indent(pformat(res), TAB)}\n")
            if checks:
                print("Checks")
                for check in checks:
                    res = check()
                    print(f"Result\n{indent(pformat(res), TAB)}")

            print('-'*100)

        except AssertionError:
            print("Invalid input")


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='Cassanrda query executor')
    parser.add_argument('action', type=str, choices=actions, help="One of the actions available")

    args = parser.parse_args()

    store = Store([SEED_NODE], PORT, KEYSPACE, EXEC_PROFILES)
    try:
        actions[args.action]()
    except KeyboardInterrupt:
        pass
    finally:
        store.close()
        print("\nExit")
