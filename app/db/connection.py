import os
from dotenv import load_dotenv
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager


load_dotenv

database_uri = os.environ['DATABASE_URI']

pool = SimpleConnectionPool(minconn=1, maxconn=2, dsn=database_uri)

@contextmanager
def get_connection():
    connection = pool.getconn()

    try:
        yield connection
    finally:
        pool.putconn(connection)