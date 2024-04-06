import os
import sys
from contextlib import contextmanager

import psycopg
from dotenv import load_dotenv

sys.path.append('..')
from timer import measure
from logger import get_logger


load_dotenv()
host = os.environ["POSTGRES_HOST"]
port = os.environ["POSTGRES_PORT"]
db = os.environ["POSTGRES_DB"]
user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]

logger = get_logger('postgres')


@contextmanager
def get_conn(commit=False) -> (psycopg.Connection, psycopg.cursor):
    with psycopg.connect(autocommit=commit,
                         host=host,
                         port=port,
                         dbname=db,
                         user=user,
                         password=password) as conn, conn.cursor() as cur:
        yield conn, cur

        conn.commit()


@measure('LostUpdate process')
def lost_update(n):
    user_id = 1
    with get_conn() as (conn, cur):
        for _ in range(n):
            with conn.transaction():
                cur.execute("""SELECT counter FROM user_counter WHERE user_id = %s""", (user_id,))
                counter = cur.fetchone()[0] + 1
                cur.execute("""UPDATE user_counter SET counter = %s WHERE user_id = %s""", (counter, user_id))


@measure('In-place Update process')
def in_place_update(n):
    user_id = 1
    with get_conn() as (conn, cur):
        for _ in range(n):
            with conn.transaction():
                cur.execute("""UPDATE user_counter SET counter = counter + 1 WHERE user_id = %s""", (user_id,))


@measure('Row-level locking process')
def row_level_locking(n):
    user_id = 1
    with get_conn() as (conn, cur):
        for _ in range(n):
            with conn.transaction():
                cur.execute("""SELECT counter FROM user_counter WHERE user_id = %s FOR UPDATE""", (user_id,))
                counter = cur.fetchone()[0] + 1
                cur.execute("""UPDATE user_counter SET counter = %s WHERE user_id = %s""", (counter, user_id))


@measure("OCC process")
def occ(n):
    """Optimistic concurrency control method"""
    user_id = 1
    with get_conn() as (conn, cur):
        for _ in range(n):
            while True:
                with conn.transaction():
                    cur.execute("""SELECT counter, version FROM user_counter WHERE user_id = %s""", (user_id, ))
                    counter, version = cur.fetchone()
                    cur.execute("""UPDATE user_counter SET counter = %s,version = %s WHERE user_id = %s AND version = %s""",
                                (counter + 1, version + 1, user_id, version))

                if cur.rowcount: break


def get_result():
    user_id = 1
    with get_conn() as (_, cur):
        cur.execute("""
            SELECT counter FROM user_counter WHERE user_id = %s
        """, (user_id,))

        logger.info(f"Postgres `user_counter` result: {cur.fetchone()[0]}")


def reset_db():
    with get_conn(commit=True) as (conn, cur):
        with open('user_counter.sql') as sql:
            cur.execute(sql.read())


methods = {
    'lost_update': dict(method=lost_update, pre=reset_db, post=get_result),
    'in_place_update': dict(method=in_place_update, pre=reset_db, post=get_result),
    'row_level_locking': dict(method=row_level_locking, pre=reset_db, post=get_result),
    'occ': dict(method=occ, pre=reset_db, post=get_result)
}


if __name__ == '__main__':
    import time
    import argparse
    from executor import ProcessExecutor

    parser = argparse.ArgumentParser(description='Postgres DB counter update methods')
    parser.add_argument('--method', type=str, choices=methods, action='append', dest='methods', required=False, help='Method of incrementing the counter from multiple connections')
    parser.add_argument('--connections', type=int, default=10, required=False, help="Number of simultaneous `connections` (process workers)")
    parser.add_argument('--iters', type=int, default=10_000, required=False, help="Number of counter increment requests from each `connection`")

    args = parser.parse_args()
    for method in (args.methods or methods):
        executor = ProcessExecutor(**methods[method], workers=args.connections)
        executor.run(args.iters)
        time.sleep(5)
