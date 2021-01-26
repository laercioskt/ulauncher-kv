import logging
import os
import sqlite3

_db_ = os.getenv("HOME") + "/.kv.db"
_LOGGER_ = logging.getLogger(__name__)


class DataBase():
    """ Abstraction of the database using sqlite """

    def __init__(self):
        """ Create de data base if not exists """

        connection = sqlite3.connect(_db_)

        statementVersionTable = '''CREATE TABLE IF NOT EXISTS DB_VERSION ( VERSION INTEGER NOT NULL );'''
        connection.execute(statementVersionTable)

        version = connection.execute('select VERSION from DB_VERSION').fetchone()
        _LOGGER_.debug("VERSION = {}".format(version))

        if version is None:
            self.execute_statement('''CREATE TABLE IF NOT EXISTS KV ( KEY TEXT NOT NULL, VALUE TEXT NOT NULL );''')
            self.execute_statement('''insert into DB_VERSION values (1);''')

        if version[0] is 1:
            self.execute_statement('''ALTER TABLE KV ADD COLUMN TAGS TEXT NULL;''')
            self.execute_statement('''update DB_VERSION set VERSION = 2;''')

        version = connection.execute('select VERSION from DB_VERSION').fetchone()
        if version[0] is not 2:
            _LOGGER_.debug("VERSION WRONG = {}".format(version))

    def execute_statement(self, statement):
        """ Execute a query, returning dataset and commit the statemente """

        connection = sqlite3.connect(_db_)
        result = connection.execute(statement)
        connection.commit()
        return result
