import pygetwindow as gw
class WindowManager:
    def get_active_window(self):
        win = gw.getActiveWindow()
        return {"title": win.title if win else "Unknown"}
    def list_windows(self):
        return [{"title": w.title} for w in gw.getAllWindows()]
