import sys
from pprint import pformat

sys.path.append('..')
import logger
from main import MongoCollection


recorder = logger.get_logger(name='task', fmt='%(message)s')


items_tasks = {
    '1' : lambda: (items.insert_many('items.json'),                                                                                     "Populate the DB with items"),
    '2' : lambda: (items.find(None, projection='all'),                                                                                  "Get all items with all fields returned"),
    '3' : lambda: (items.find("(category == 'TV').count()"),                                                                            "Count items in TV category"),
    '4' : lambda: (items.find("category.distinct().count()"),                                                                           "Count number of distinct categories"),
    '5' : lambda: (items.find("brand.distinct()"),                                                                                      "Get all distinct brands"),
    '6a': lambda: (items.find("(category == 'Laptops') & (price.between(300, 1500))", projection='all'),                                "Get items in category Laptops in price 300-1500 ($and operator"),
    '6b': lambda: (items.find("(model == 'S12 Ultra') | (model == 'iPhone 13')", projection='all'),                                     "Get items either of model queried ($or operator)"),
    '6c': lambda: (items.find("brand.in_('Apple', 'Samsung', 'GameTech')", projection='all'),                                           "Get items of brands listed ($in operator)"),
    '7' : lambda: (items.update("storage.in_('1TB SSD', '512GB SSD')", update_query="(RAM == '64GB') & (warranty == '5 years')"),       "Update items with queried storage value by changing RAM and adding a new prop - warranty"),
    '8' : lambda: (items.update("water_resistance.exists()", update_query="price + 300"),                                               "Get items which have water_resistance prop & update them by incrementing price on 300"),
}

orders_tasks = {
    '1' : lambda: (MongoCollection._populate(),                                                                                                     "Populate items & orders collections"),
    '2' : lambda: (orders.find(None, projection='all'),                                                                                             "Get all orders with all fields returned"),
    '3' : lambda: (orders.find("total_sum > 1000"),                                                                                                 "Get orders with the total cost more than 1000"),
    '4' : lambda: (orders.find("(customer.name == 'Jessica') & (customer.surname == 'Anderson')"),                                                  "Get all orders made by Jessica Anderson"),
    '5' : lambda: (orders.find("""items_id.join('items._id', 'brand == "Apple"', alias='ordered')""", projection='all'),                            "Get all orders with Apple products"),
    '6' : lambda: (__orders_task_6(),                                                                                                               "Add the FitBand watch to all orders with cost above 1500 and update the total cost"),
    '7' : lambda: (orders.find("(customer.name == 'Michael').count('items_id')"),                                                                   "Count a number of items in the orders made by Michael"),
    '8' : lambda: (orders.find("total_sum > 1200", projection="customer,payment.cardId,total_sum"),                                                 "Show customer and payment info in orders with the total cost above 1200"),
    '9' : lambda: (orders.update(
        """(date.between('2024-01-01', '2024-12-31')).join('items._id', on='items_id', where="model == 'iPhone 13'", alias='ordered')""",
        update_query="items_id - [ordered[0]['_id']]"
        ),                                                                                                                                          "Remove orders with iPhone 13 in it made within the 2024 year"),
    '10': lambda: (orders.update("customer.surname == 'Durden'", update_query="(customer.name == 'Tyler') & (payment.card_owner[0] == 'Tyler')"),   "Rename the customer name which surname is Durden"),
    '11': lambda: (orders.find(
        "(payment.card_owner == ['Michael', 'Brown']).join('items._id', on='items_id', alias='items')",
        projection="customer,items.brand,items.price"),                                                                                             "Show customer info, items model and price in orders made by the same customer (Michael Brown)")
}

review_tasks = [
    lambda: (MongoCollection._populate(),                                                                                                                                   "Populate the DB with items and orders"),
    lambda: (MongoCollection('last_reviews', capped=True, size=10*1024**2, max=5).info(),                                                                                          "Creation of a capped collection `last_reviews` with size=5", ),
    lambda: (__reviews_task_2(),                                                                                                                                            "Populating the `last_reviews` collection with 5 different reviews"),
    lambda: (MongoCollection('last_reviews').insert({"author": "Anonymous User 2", "rate": 5, "text": "Liked that site so much! Definitely buy something here someday"}),   "Adding 6-th review to the capped collection"),
    lambda: (MongoCollection('last_reviews').find(None, projection='all'), MongoCollection('last_reviews').find("_id.count()", projection='count'),                         "Checking that when the limit is reached, the old reviews are deleted"),
]


def __orders_task_6():
    item_to_add = items.find("model == 'FitBand 500'", projection='id_,price')
    items_id, prices = zip(*[o.values() for o in item_to_add])

    return orders.update(
        'total_sum >= 1500',
        update_query=f"(items_id + {items_id}) & (total_sum + {sum(prices)})"
    )


def __reviews_task_2():
    customers = orders.find("customer.distinct('customer.name', 'customer.surname')")
    reviews = [
        {"author": ' '.join(customers[0]['field']), "rate": 5, "text": "Love shopping here! Easy website, quick delivery, top-notch products."},
        {"author": ' '.join(customers[1]['field']), "rate": 3, "text": "Average experience: okay site, high shipping, return hassle."},
        {"author": ' '.join(customers[2]['field']), "rate": 4, "text": "Positive overall: user-friendly site, vast selection, prompt delivery."},
        {"author": ' '.join(customers[3]['field']), "rate": 2, "text": "Disappointed: confusing site, slow delivery, not worth the hassle."},
        {"author": "Anonymous User",                "rate": 1, "text": "Worst experience ever! Glitchy website, misleading info, no support."},
    ]
    last_reviews = MongoCollection('last_reviews')
    for rev in reviews:
        last_reviews.insert(rev)

    return MongoCollection('last_reviews').find(None, projection='all')


tasks = {
    'items': items_tasks,
    'orders': orders_tasks,
    'last_reviews': review_tasks
}


def __arbitrary_exec(collection, tasks):
    recorder.info(f"`{collection}` available tasks: {tuple(tasks)}")
    while True:
        task_number = input("Enter task number [leave empty to exit]: ")
        if not task_number: break
        if task_number not in tasks:
            print('Invalid task number')
            continue

        task = tasks[task_number]
        recorder.info(f"{task_number:-^100}")
        *res, desc = task()
        recorder.info(desc + "\n")
        [recorder.info(pformat(r)) for r in res]
        recorder.info("-" * 100)
        print(f"`{collection}` available tasks: {tuple(tasks)}")


def __sequential_exec(collection, steps):
    recorder.info(f"`{collection}` task steps: {tuple(range(1, len(steps)))}")
    for step_n, task in enumerate(steps):
        input(f"Press any key -> {step_n+1} step: ")
        recorder.info(f"{step_n+1:-^100}")
        *res, desc = task()
        recorder.info(desc + "\n")
        [recorder.info(pformat(r)) for r in res]
        recorder.info("-" * 100)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='MongoDB task executor')
    parser.add_argument('collection', choices=tasks, type=str, help='MongoDB collection name')
    parser.add_argument('--record', action='store_true', help='Whether or not to write the output to a file')
    args = parser.parse_args()

    orders = MongoCollection('orders')
    items = MongoCollection('items')

    recorder = recorder \
        if not args.record \
        else logger.get_file_logger(name=f"{args.collection}_tasks", filename=f"{args.collection}_tasks.log", fmt='%(message)s')

    try:
        tasks_to_execute = tasks[args.collection]
        if isinstance(tasks_to_execute, list):
            __sequential_exec(args.collection, tasks_to_execute)
        elif isinstance(tasks_to_execute, dict):
            __arbitrary_exec(args.collection, tasks_to_execute)
    except Exception as e:
        print(f"Error is occurred - {e}")
    except KeyboardInterrupt:
        recorder.info("\nExit")
    finally:
        orders.drop()
        items.drop()
        MongoCollection('last_reviews').drop()
