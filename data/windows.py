import subprocess
import json


class WindowsService:
    @staticmethod
    def get_all_windows():
        QUERY = "gdbus call --session --dest org.gnome.Shell --object-path /org/gnome/Shell/Extensions/Windows --method org.gnome.Shell.Extensions.Windows.List"
        result = subprocess.run(QUERY, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return []
        
        windows = result.stdout.replace("('", '').replace("',)", '')
        return json.loads(windows)