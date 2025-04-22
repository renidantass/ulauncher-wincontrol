import os
import configparser
from gi.repository import Gtk
from .desktop_file_manager import DesktopFileManager

class IconManager:
    @staticmethod
    def get_icon_from_desktop(desktop_file) -> str | None:
        if desktop_file is None:
            return 'images/icon.png'

        config = configparser.ConfigParser()
        config.read(desktop_file)
        icon_name = config['Desktop Entry']['Icon']

        theme = Gtk.IconTheme.get_default()
        theme.append_search_path('/var/lib/flatpak/exports/share/icons/')
        theme.append_search_path(os.path.expanduser('~/.local/share/flatpak/exports/share/icons/'))
        theme.append_search_path('/snap/')

        icon = theme.lookup_icon(icon_name, 48, 0)
        return icon.get_filename() if icon else 'images/icon.png'
    
    @staticmethod
    def get_icon_from_wm_class(wm_class):
        desktop = DesktopFileManager.get_file_by_wm_class(wm_class)
        return IconManager.get_icon_from_desktop(desktop)
