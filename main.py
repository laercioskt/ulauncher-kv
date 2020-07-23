import sqlite3
import os
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

_icon_ = "images/icon.svg"
_db_ = os.getenv("HOME") + "/.testetestes.db"
_name_ = "Kv"


class KvExtension(Extension):

    def __init__(self):
        super(KvExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        connection = sqlite3.connect(_db_)
        statement = '''CREATE TABLE IF NOT EXISTS KV ( KEY TEXT NOT NULL, VALUE TEXT NOT NULL );'''
        connection.execute(statement)


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        arguments = (event.get_query().get_argument() or "").split()
        if self.is_get(arguments):
            return RenderResultListAction(self.get_action(""))
        if self.is_get_with_filter(arguments):
            return RenderResultListAction(self.get_action(arguments[1]))
        if self.is_unset(arguments):
            return RenderResultListAction(self.get_unset_action(arguments[1]))
        if self.is_set(arguments):
            return RenderResultListAction(self.set_action(arguments[1], arguments[2]))
        else:
            return RenderResultListAction(self.default_action())

    def is_get(self, arguments):
        return len(arguments) == 1 and arguments[0] == "get"

    def is_get_with_filter(self, arguments):
        return len(arguments) == 2 and arguments[0] == "get"

    def is_unset(self, arguments):
        return len(arguments) == 3 and arguments[0] == "get" and arguments[2] == "unset"

    def is_set(self, arguments):
        return len(arguments) == 3 and arguments[0] == "set"

    def set_action(self, key, value):
        connection = sqlite3.connect(_db_)
        item = ExtensionResultItem(icon=_icon_, name="{} = {}".format(key, value))
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
                icon=_icon_, 
                name="{} = {}".format(key, value),
                description="Press enter or click to copy '{}' to clipboard or type 'unset' to unset from db".format(value),
                on_enter=CopyToClipboardAction(value))
            items.append(item)

        if not exists:
            item = ExtensionResultItem(icon=_icon_, name=_name_)
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
        item = ExtensionResultItem(icon=_icon_, name=_name_)
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
                icon=_icon_,
                name=_name_, 
                description="Enter a query in the form of \"[set] <key> <value> | [get] <key>; [unset]\"")
        ]


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        return RenderResultListAction(
            [ExtensionResultItem(
                icon=_icon_,
                name=_name_,
                description="Enter a query in the form of \"[set] <key> <value> | [get] <key>; [unset]\"")])


if __name__ == '__main__':
    KvExtension().run()
