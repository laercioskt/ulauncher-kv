import logging

from constant import ICON, NAME

from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction


_LOGGER_ = logging.getLogger(__name__)


class DefatulAction(): 
    def __init__(self):
        None

    def execute(self):
        _LOGGER_.debug("Executing DefatulAction")
        return [ ExtensionResultItem(icon=ICON, name=NAME, description="Enter: \"[set] <key> <value> | [get] <key>; [unset] | (or just) <key>\"") ]

class GetAction():
    def __init__(self, db, text):
       self.text = text
       self.db = db

    def execute(self):
        _LOGGER_.debug("Executing GetAction")
        items = []
        exists = 0
        for row in self.db.execute_statement("SELECT key, value, tags from KV where key like '%{}%' or tags like '%{}%'".format(self.text, self.text)):
            exists = 1
            key = row[0]
            value = row[1]
            value_fix = value.strip().replace('$','\$').replace('"','\\"').replace('`','\\`') + '\n'
            script_action  = 'sleep 0.01m && echo -n "' + value_fix + '" | xclip -i -selection clipboard && sleep 0.01m && xdotool key --clearmodifiers ctrl+v &'
            item = ExtensionResultItem(
                icon=ICON,
                name="{} = {}".format(key, value),
                description="Press enter or click to copy '{}' to clipboard or type 'unset' to unset from db".format(value),
                on_alt_enter=RunScriptAction(script_action, []),
                on_enter=CopyToClipboardAction(value))
            items.append(item)

        if not exists:
            item = ExtensionResultItem(icon=ICON, name=NAME)
            if self.text == "":
                item._description = "It looks like you have nothing stored"
            else:
                item._description = "No VALUE for KEY: '{}'".format(self.text)
            items.append(item)

        return items

class UnsetAction():
    def __init__(self, db, key):
        self.key_filter = key
        self.db = db

    def execute(self):
        _LOGGER_.debug("==== Executing UnsetAction")
        exists = 0
        statement = "SELECT key, value, tags from KV where key = '{}'".format(self.key_filter)
        key = ""
        value = ""
        for row in self.db.execute_statement(statement):
            exists = 1
            key = row[0]
            value = row[1]
        item = ExtensionResultItem(icon=ICON, name=NAME)
        if exists:
            item._description = "Key '{}' of Value '{}' unset".format(key, value)
            statement = "DELETE FROM KV WHERE KEY = '{}'".format(key)
            self.db.execute_statement(statement)
        else:
            item._description = "'{}' not found to unset".format(self.key_filter)
        return [item]

class SetAction():
    def __init__(self, db, key, value):
        self.key = key
        self.value = value
        self.db = db

    def execute(self):
        _LOGGER_.debug("==== Executing SetAction")
        item = ExtensionResultItem(icon=ICON, name="{} = {}".format(self.key, self.value))
        cursor = self.db.execute_statement("SELECT key, value, tags from KV where key = '{}'".format(self.key))
        exists = 0
        for _ in cursor:
            exists = 1
            break
        if exists:
            statement = "UPDATE KV SET VALUE = '{}' WHERE KEY = '{}'".format(self.value, self.key)
            item._description = "Update '{}' with '{}'".format(self.key, self.value)
        else:
            statement = "INSERT INTO KV (KEY,VALUE) VALUES ('{}', '{}')".format(self.key, self.value)
            item._description = "Insert '{}' with '{}'".format(self.key, self.value)
        self.db.execute_statement(statement)
        _LOGGER_.debug("Insert '{}' with '{}'".format(self.key, self.value))
        return [item]

class ActionFactory():

    def __init__(self, arguments, db):
        self.arguments = arguments
        self.db = db
       
    def create(self):
        if self.is_get_without_filter(self.arguments):
            text = self.arguments[0] if len(self.arguments) == 1 else ""
            return GetAction(self.db, text)
        if self.is_get_with_filter(self.arguments):
            return GetAction(self.db, self.arguments[1])
        if self.is_set(self.arguments):
            return SetAction(self.db, self.arguments[1], ' '.join(self.arguments[2:]))
        if self.is_unset(self.arguments):
            return UnsetAction(self.db, self.arguments[1])
        else:
            return DefatulAction()

    def is_get_without_filter(self, arguments):
        return ( len(arguments) == 1 and arguments[0] == "get" ) or ( len(arguments) == 1 and arguments[0] != "set" )

    def is_get_with_filter(self, arguments):
        return len(arguments) == 2 and arguments[0] == "get"

    def is_set(self, arguments):
        return len(arguments) >= 3 and arguments[0] == "set"

    def is_unset(self, arguments):
        return len(arguments) == 3 and arguments[0] == "get" and arguments[2] == "unset"
