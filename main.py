import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from data.windows import WindowsService


logger = logging.getLogger()


class WinControlExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        windows = WindowsService().get_all_windows()
        for i in range(0, len(windows)):
            logger.debug(windows[i])
            window_title = windows[i]['title']
            data = {'title': window_title}
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name='%s' % window_title,
                                             on_enter=ExtensionCustomAction(data, keep_app_open=True)))

        return RenderResultListAction(items)
    
class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        data = event.get_data()
        logger.debug(data)
        WindowsService().focus_in_window(data['title'])

if __name__ == '__main__':
    WinControlExtension().run()