from flask import g
import sqlite3
import os


    
def connect_db():
    """
    The function `connect_db` connects to a SQLite database named "members.db" located in the current
    working directory.
    :return: The `connect_db` function returns a connection to a SQLite database named "members.db"
    located in the current working directory. The function sets the row factory to `sqlite3.Row` before
    returning the connection.
    """
    current_path = os.getcwd()
    db_name = "members.db"
    sql = sqlite3.connect(f"{current_path}/{db_name}")
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    """
    The function `get_db` returns a connection to a SQLite database if it exists, otherwise it creates a
    new connection.
    :return: The function `get_db()` is returning the SQLite database connection object `g.sqlite_db`.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
