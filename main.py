import logging

from constant import ICON, NAME
from db import DataBase
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from actions import ActionFactory

_LOGGER_ = logging.getLogger(__name__)


class KvExtension(Extension):

    def __init__(self):
        super(KvExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        self.db = DataBase()
        _LOGGER_.debug("KV Extension DataBase Done")

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        _LOGGER_.debug("KeywordQueryEventListener executing")
        arguments_or_empty: str = event.get_query().get_argument() or ""
        arguments: list = arguments_or_empty.split()
        return RenderResultListAction(ActionFactory(arguments, extension.db).create().execute())

class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        _LOGGER_.debug("ItemEnterEventListener executing")
        return RenderResultListAction([ExtensionResultItem(icon=ICON, name=NAME, description="Enter: \"[set] <key> <value> | [get] <key>; [unset] | (or just) <key>\"")])


if __name__ == '__main__':
    KvExtension().run()
