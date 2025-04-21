import subprocess
import json


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