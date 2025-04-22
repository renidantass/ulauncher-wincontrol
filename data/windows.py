import subprocess
import json
import os
import configparser
import gi
from gi.repository import Gtk


class WindowsService:
    @staticmethod
    def get_all_windows() -> list[dict]:
        QUERY = "gdbus call --session --dest org.gnome.Shell --object-path /org/gnome/Shell/Extensions/Windows --method org.gnome.Shell.Extensions.Windows.List"
        result = subprocess.run(QUERY, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return []
        
        windows = result.stdout.replace("('", '').replace("',)", '')
        return json.loads(windows)
    
    @staticmethod
    def focus_in_window(title: str) -> bool | None:
        QUERY = f"""busctl --user call \
    org.gnome.Shell \
    /de/lucaswerkmeister/ActivateWindowByTitle \
    de.lucaswerkmeister.ActivateWindowByTitle \
    activateBySubstring \
    s '{title}'"""
        result = subprocess.run(QUERY, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            return False
        
        raw_response = result.stdout.replace('b', '').strip()
        response = {"true": True, "false": False}.get(raw_response.lower())
        return response
    
    @staticmethod
    def get_file_desktop_by_wm_class(wm_class: str) -> str | None:
        possible_directories = [
            os.path.expanduser('~/.local/share/applications/'),
            '/usr/share/applications',
            os.path.expanduser('~/.local/share/flatpak/exports/share/applications'),
            '/var/lib/flatpak/exports/share/applications',
            '/var/lib/snapd/desktop/applications'
        ]

        for directory in possible_directories:
            if not os.path.exists(directory):
                continue
            # Busca por nome de arquivo (ex: org.gnome.TextEditor.desktop)
            desktop_path = os.path.join(directory, f"{wm_class}.desktop")
            if os.path.exists(desktop_path):
                return desktop_path
            
            # Se não encontrou, busca por StartupWMClass nos arquivos .desktop
            for filename in os.listdir(directory):
                if not filename.endswith('.desktop'):
                    continue
                path = os.path.join(directory, filename)
                config = configparser.ConfigParser()
                try:
                    config.read(path)
                    startup_wm_class = config.get('Desktop Entry', 'StartupWMClass', fallback='')
                    if startup_wm_class.lower() == wm_class.lower():
                        return path
                except Exception:
                    continue
        return None
            
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
        desktop = WindowsService().get_file_desktop_by_wm_class(wm_class)
        icon_path = WindowsService().get_icon_from_desktop(desktop)
        return icon_path