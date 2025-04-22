import os
import configparser

class DesktopFileManager:
    @staticmethod
    def get_file_by_wm_class(wm_class: str) -> str | None:
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
            desktop_path = os.path.join(directory, f"{wm_class}.desktop")
            if os.path.exists(desktop_path):
                return desktop_path
            
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
