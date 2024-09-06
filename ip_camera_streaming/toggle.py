import sys
import subprocess
import keyboard  # For hotkey detection
import win32gui
import win32con

class AppSwitcher:
    def __init__(self):
        # Paths to your executables
        self.camera_app_path = "path/to/your/camera_app.exe" 
        self.flutter_app_path = "path/to/your/flutter_app.exe"

        # Start both apps (initially hidden)
        self.camera_app_process = subprocess.Popen([self.camera_app_path], creationflags=win32con.CREATE_NO_WINDOW)
        self.flutter_app_process = subprocess.Popen([self.flutter_app_path], creationflags=win32con.CREATE_NO_WINDOW)

        # Set initial active app (e.g., camera app)
        self.active_app = "camera"
        self.show_app(self.camera_app_process)
        self.hide_app(self.flutter_app_process)

        # Set up hotkey (e.g., Ctrl + Shift + T)
        keyboard.add_hotkey("ctrl+shift+t", self.toggle_apps)

    def show_app(self, process):
        hwnd = self.find_window(process.pid)
        if hwnd:
            win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
            win32gui.SetForegroundWindow(hwnd)

    def hide_app(self, process):
        hwnd = self.find_window(process.pid)
        if hwnd:
            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

    def find_window(self, pid):
        def enum_windows_proc(hwnd, lparam):
            if win32gui.GetWindowThreadProcessId(hwnd)[1] == pid:
                lparam[0] = hwnd
                return False  # Stop enumeration
            return True

        hwnd = [0]
        win32gui.EnumWindows(enum_windows_proc, hwnd)
        return hwnd[0]

    def toggle_apps(self):
        if self.active_app == "camera":
            self.hide_app(self.camera_app_process)
            self.show_app(self.flutter_app_process)
            self.active_app = "flutter"
        else:
            self.hide_app(self.flutter_app_process)
            self.show_app(self.camera_app_process)
            self.active_app = "camera"

if __name__ == "__main__":
    switcher = AppSwitcher()
    keyboard.wait()  # Keep the script running to listen for hotkey