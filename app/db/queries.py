import os
from dotenv import load_dotenv
from functools import wraps
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager

from werkzeug.security import check_password_hash


load_dotenv()

database_uri = os.environ['DATABASE_URI']

pool = SimpleConnectionPool(minconn=1, maxconn=2, dsn=database_uri)

@contextmanager
def get_connection():
    connection = pool.getconn()

    try:
        yield connection
    finally:
        pool.putconn(connection)

@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor

class User:
    def __init__(self, id, username, pwdhash):
        self.id = id
        self.username = username
        self.pwdhash = pwdhash

    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)
    
    def __repr__(self):
        return f'<User "{self.username}">'
    

CHECK_LOGIN = "SELECT * FROM users WHERE username = (%s);"
GET_USER = "SELECT * FROM users WHERE id = (%s);"
GET_PROJECTS = "SELECT name, link, description FROM portfolio;"
INSERT_PROJECT = "INSERT INTO portfolio (name,link,description) VALUES (%s,%s,%s);"


def get_user_object(id):
    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(GET_USER, (id,))
            user = cursor.fetchone()
            if user:
                return User(user[0],user[1],user[2])


def validate_user(username, password):
    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(CHECK_LOGIN, (username,))
            user = cursor.fetchone()
            if user and check_password_hash(user[2],password):
                return user[0]
            

def all_projects():
    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(GET_PROJECTS)
            projects = cursor.fetchall()
            return projects
            

def create_project(name, link, description):
    with get_connection() as connection:
        with get_cursor(connection) as cursor:
            cursor.execute(INSERT_PROJECT,(name,link,description))