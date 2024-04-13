import os
import sys
from contextlib import contextmanager

try:
    import pyvis
except ImportError:
    pass

from tabulate import tabulate
from dotenv import load_dotenv
from neo4j import GraphDatabase, Result

from queries import query_dict, node_props, formats
sys.path.append('..')
from logger import get_file_logger


load_dotenv()
URI = "bolt://localhost:7687"
AUTH = tuple(os.environ['NEO4J_AUTH'].split('/'))
DEFAULT_DB = "neo4j"

logger = get_file_logger('bookstore', filename='neo4j.log', fmt="%(message)s")


@contextmanager
def get_conn():
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()

        yield driver


def execute_query(query, graph=False, **kwargs):
    result_transformer = Result.to_eager_result if not graph else Result.graph
    with get_conn() as driver:
        return driver.execute_query(
            query,
            **kwargs,
            database_=DEFAULT_DB,
            result_transformer_=result_transformer
        )


def create_graph(filename):
    with open(filename) as cypher_file:
        _, summary, _ = execute_query(cypher_file.read())
        print(summary.counters)


def delete_graph():
    _, summary, _ = execute_query("""MATCH (n) DETACH DELETE n""")
    print(summary.counters)


formatters = {
    "table": lambda res: __output_as_table(res),
    "graph": lambda res: __output_as_graph(res),
}
actions = {
    "create-graph": lambda: create_graph("cypher/BOOKSTORE_GRAPH.cypher"),
    "delete-graph": lambda: delete_graph(),
    "run": lambda: __run_interactive_mode()
}
prompts = {
    "get_customer_orders_info": lambda: input("Enter customer name: "),
    "get_customer_orders_grouped_by_date": lambda: input("Enter customer name: "),
    "sum_price_for_customer": lambda: input("Enter customer name: "),
    "get_viewed_books_by_customer": lambda: input("Enter customer name: "),
    "get_viewed_not_bought_books_by_customer": lambda: input("Enter customer name: "),
    "recommend_same_author_books_by_viewed": lambda: input("Enter customer name: "),
    "recommend_similar_books_based_on_customer_orders": lambda: input("Enter customer name: "),
    "get_books_bought_together_with_book": lambda: input("Enter book title: "),
    "get_customer_info_by_book_ordered": lambda: input("Enter book title: "),
    "get_orders_by_date": lambda: input("Enter date YYYY-MM-DD format: "),
}


def __output_as_table(result):
    records, summary, keys = result
    logger.info(f"Query {summary.query}\nwith parameters {summary.parameters} --->\n")
    if records:
        logger.info(tabulate([rec.data() for rec in records], headers='keys', tablefmt='outline', showindex=range(1, len(records) + 1)))
    else:
        logger.info(tabulate([], headers=keys, tablefmt='outline'))

    logger.info("")


def __output_as_graph(graph):
    visual_graph = pyvis.network.Network()

    for node in graph.nodes:
        node_label = list(node.labels)[0]
        node_text = node[node_props[node_label]]
        visual_graph.add_node(node.element_id, node_text, group=node_label)

    for relationship in graph.relationships:
        visual_graph.add_edge(
            relationship.start_node.element_id,
            relationship.end_node.element_id,
            title=f"{relationship.type} {dict(relationship.items()) or ' '}"
        )

    visual_graph.show('graph.html', notebook=False)


def __run_interactive_mode():
    cases = list(query_dict)
    menu = '\n'.join(f"[{i + 1:2}]: {case}" for i, case in enumerate(cases))
    logger.info(menu)
    while True:
        try:
            choice = input("Enter a case number (leave empty to exit/`h` to show cases): ").lower()
            if not choice: break
            if choice == 'h':
                print(menu)
                continue

            case = cases[int(choice) - 1]
            query = query_dict[case]
            query_variants = tuple(query.keys())
            if len(query_variants) == 1:
                format_ = query_variants[0]
                in_graph = format_ == 'graph'
            else:
                in_graph = input("Output in graph? (Y/y/yes) (if no, output in table): ").lower() in ('y', 'yes')
                format_ = formats[in_graph]

            logger.info(f"The specified query`s result will be formatted in the `{format_}` view")
            logger.info(f"{case:-^100}")
        except (ValueError, IndexError):
            print('Invalid input')
            continue

        prompt = prompts.get(case)
        values = {"value": prompt()} if prompt is not None else {}
        result = execute_query(query[format_], graph=in_graph, **values)

        formatters[format_](result)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Neo4j query executor')
    parser.add_argument('action', type=str, choices=actions, help="One of the actions available")

    args = parser.parse_args()

    try:
        actions[args.action]()
    except KeyboardInterrupt:
        pass
    finally:
        print("\nExit")
