import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from services.window_manager import WindowManager
from services.icon_manager import IconManager


logger = logging.getLogger()

class WinControlExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        self.subscribe(KeywordQueryEvent, CloseWindowQueryEventListener())  # Novo listener para `wc`

class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        windows = WindowManager.get_all_windows()
        for window in windows:
            logger.debug(window)
            window_title = window['title']
            wm_class = window['wm_class']
            window_icon = IconManager.get_icon_from_wm_class(wm_class)
            data = {'title': window_title}
            items.append(ExtensionResultItem(icon=window_icon,
                                             name='%s' % window_title,
                                             on_enter=ExtensionCustomAction(data, keep_app_open=True)))

        return RenderResultListAction(items)
    
class CloseWindowQueryEventListener(EventListener):
    def on_event(self, event, extension):
        if event.get_keyword() != "wc":
            return

        items = []
        windows = WindowManager.get_all_windows()
        for window in windows:
            logger.debug(window)
            window_title = window['title']
            pid = window['pid']
            wm_class = window['wm_class']
            window_icon = IconManager.get_icon_from_wm_class(wm_class)
            data = {'pid': pid}
            items.append(ExtensionResultItem(icon=window_icon,
                                             name='%s' % window_title,
                                             on_enter=ExtensionCustomAction(data, keep_app_open=False)))

        return RenderResultListAction(items)

class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        data = event.get_data()

        if data.get('pid'):
            WindowManager.close_window(data['pid'])
        else:
            WindowManager.focus_in_window(data['title'])

if __name__ == '__main__':
    WinControlExtension().run()