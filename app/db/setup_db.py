from werkzeug.security import generate_password_hash

import queries


CREATE_USERS = """CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(20) UNIQUE,
    pwdhash TEXT
);"""
CREATE_PORTFOLIO = """CREATE TABLE IF NOT EXISTS portfolio(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    link TEXT NOT NULL,
    description TEXT NOT NULL
)"""
CREATE_BADGES = """CREATE TABLE IF NOT EXISTS badges(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    link TEXT NOT NULL,
    filename TEXT NOT NULL
)"""

ADD_USER = "INSERT INTO users (username,pwdhash) values (%s,%s);"


username = input('Enter username: ')
password = input('Enter password: ')

pwdhash = generate_password_hash(password)

with queries.get_connection() as connection:
    with queries.get_cursor(connection) as cursor:
        cursor.execute(CREATE_USERS)
        cursor.execute(CREATE_PORTFOLIO)
        cursor.execute(CREATE_BADGES)
        cursor.execute(ADD_USER, (username,pwdhash))