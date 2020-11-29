import os
import sqlite3

_db_ = os.getenv("HOME") + "/.kv.db"


class DataBase():
    """ Abstraction of the database using sqlite """

    def __init__(self):
        """ Create de data base if not exists """

        connection = sqlite3.connect(_db_)
        statement = '''CREATE TABLE IF NOT EXISTS KV ( KEY TEXT NOT NULL, VALUE TEXT NOT NULL );'''
        connection.execute(statement)

    def execute_statement(self, statement):
        """ Execute a query, returning dataset and commit the statemente """

        connection = sqlite3.connect(_db_)
        result = connection.execute(statement)
        connection.commit()
        return result
