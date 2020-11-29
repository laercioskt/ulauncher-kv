import os
import sqlite3
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

_db_ = os.getenv("HOME") + "/.kv.db"


class DataBase():

    def __init__(self):
        connection = sqlite3.connect(_db_)
        statement = '''CREATE TABLE IF NOT EXISTS KV ( KEY TEXT NOT NULL, VALUE TEXT NOT NULL );'''
        connection.execute(statement)

    def execute_statement(self, statement):
        connection = sqlite3.connect(_db_)
        result = connection.execute(statement)
        connection.commit()
        return result
