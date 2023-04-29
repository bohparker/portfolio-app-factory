from werkzeug.security import generate_password_hash

import connection
import queries


CREATE_USERS = """CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(20) UNIQUE,
    pwdhash TEXT
);"""
ADD_USER = "INSERT INTO users (username,pwdhash) values (%s,%s);"


username = input('Enter username: ')
password = input('Enter password: ')

pwdhash = generate_password_hash(password)

with connection.get_connection() as connection:
    with queries.get_cursor(connection) as cursor:
        cursor.execute(CREATE_USERS)
        cursor.execute(ADD_USER, (username,pwdhash))