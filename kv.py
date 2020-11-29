import os
import sqlite3
import logging
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

_ICON_ = "images/icon.svg"
_NAME_ = "Kv"
_db_ = os.getenv("HOME") + "/.kv.db"
logger = logging.getLogger(__name__)


class Actions():

    def execute(self) -> None:
        pass

    if __name__ == "__main__":
        connection = sqlite3.connect(_db_)
        statement = '''CREATE TABLE IF NOT EXISTS KV ( KEY TEXT NOT NULL, VALUE TEXT NOT NULL );'''
        connection.execute(statement)

    def set_action(self, key, value):
        connection = sqlite3.connect(_db_)
        item = ExtensionResultItem(icon=_ICON_, name="{} = {}".format(key, value))
        cursor = connection.execute("SELECT key, value from KV where key = '{}'".format(key))
        exists = 0
        for _ in cursor:
            exists = 1
            break
        if exists:
            statement = "UPDATE KV SET VALUE = '{}' WHERE KEY = '{}'".format(value, key)
            item._description = "Update '{}' with '{}'".format(key, value)
        else:
            statement = "INSERT INTO KV (KEY,VALUE) VALUES ('{}', '{}')".format(key, value)
            item._description = "Insert '{}' with '{}'".format(key, value)
        connection.execute(statement)
        connection.commit()
        logger.debug("Insert '{}' with '{}'".format(key, value))
        return [item]

    def get_action(self, key_filter):
        connection = sqlite3.connect(_db_)
        items = []
        exists = 0
        statement = "SELECT key, value from KV where key like '%{}%'".format(key_filter)
        for row in connection.execute(statement):
            exists = 1
            key = row[0]
            value = row[1]
            item = ExtensionResultItem(
                icon=_ICON_,
                name="{} = {}".format(key, value),
                description="Press enter or click to copy '{}' to clipboard or type 'unset' to unset from db".format(value),
                on_enter=CopyToClipboardAction(value))
            items.append(item)

        if not exists:
            item = ExtensionResultItem(icon=_ICON_, name=_NAME_)
            if key_filter == "":
                item._description = "It looks like you have nothing stored"
            else:
                item._description = "No VALUE for KEY: '{}'".format(key_filter)
            items.append(item)

        return items

    def get_unset_action(self, key_filter):
        connection = sqlite3.connect(_db_)
        exists = 0
        statement = "SELECT key, value from KV where key = '{}'".format(key_filter)
        key = ""
        value = ""
        for row in connection.execute(statement):
            exists = 1
            key = row[0]
            value = row[1]
        item = ExtensionResultItem(icon=_ICON_, name=_NAME_)
        if exists:
            item._description = "Key '{}' of Value '{}' unset".format(key, value)
            statement = "DELETE FROM KV WHERE KEY = '{}'".format(key)
            connection.execute(statement)
            connection.commit()
        else:
            item._description = "'{}' not found to unset".format(key_filter)
        return [item]

    def default_action(self):
        return [
            ExtensionResultItem(
                icon=_ICON_,
                name=_NAME_,
                description="Enter: \"[set] <key> <value> "
                            "| [get] <key>; [unset]\""
                            "| (or just) <key>\"")
        ]