import logging
from kv import Actions
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction

_ICON_ = "images/icon.svg"
_NAME_ = "Kv"
logger = logging.getLogger(__name__)

class KvExtension(Extension):

    def __init__(self):
        super(KvExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        self.actions = Actions()


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        arguments = (event.get_query().get_argument() or "").split()
        if self.is_get(arguments):
            filter = arguments[0] if len(arguments) == 1 else ""
            return RenderResultListAction(extension.actions.get_action(filter))
        if self.is_get_with_filter(arguments):
            return RenderResultListAction(extension.actions.get_action(arguments[1]))
        if self.is_unset(arguments):
            return RenderResultListAction(extension.actions.get_unset_action(arguments[1]))
        if self.is_set(arguments):
            return RenderResultListAction(extension.actions.set_action(arguments[1], ' '.join(arguments[2:])))
        else:
            return RenderResultListAction(extension.actions.default_action())

    def is_get(self, arguments):
        return ( len(arguments) == 1 and arguments[0] == "get" ) or ( len(arguments) == 1 and arguments[0] != "set" )

    def is_get_with_filter(self, arguments):
        return len(arguments) == 2 and arguments[0] == "get"

    def is_unset(self, arguments):
        return len(arguments) == 3 and arguments[0] == "get" and arguments[2] == "unset"

    def is_set(self, arguments):
        return len(arguments) >= 3 and arguments[0] == "set"


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        return RenderResultListAction(
            [ExtensionResultItem(
                icon=_ICON_,
                name=_NAME_,
                description="Enter: \"[set] <key> <value> | [get] <key>; [unset] | (or just) <key>\"")])


if __name__ == '__main__':
    KvExtension().run()
