import subprocess
import json

class WindowManager:
    @staticmethod
    def get_all_windows() -> list[dict]:
        QUERY = "gdbus call --session --dest org.gnome.Shell --object-path /org/gnome/Shell/Extensions/Windows --method org.gnome.Shell.Extensions.Windows.List"
        result = subprocess.run(QUERY, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return []
        
        windows = result.stdout.replace("('", '').replace("',)", '')
        windows = json.loads(windows)
        return [window for window in windows if 'ulauncher' not in window['wm_class'].lower()]
    
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
        return {"true": True, "false": False}.get(raw_response.lower())

    @staticmethod
    def close_window(pid: str) -> bool | None:
        if pid is None:
            return False

        QUERY = f"kill -9 {pid}"
        result = subprocess.run(QUERY, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return False
        
        return True
