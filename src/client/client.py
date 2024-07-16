import win32gui
import win32api
import win32process
import ctypes
from src.common.togConfig import TogConfig
from src.window_manager.window_tracker import WindowTracker
from src.common.utils import getInnnerWindows
from src.ipc.ipc import IPC
from src.ipc.message_types import MessageType

user32 = ctypes.windll.user32


class Client:
    def __init__(self):
        self.togConfig = TogConfig()
        client_title = self.togConfig.configJson.client_title
        self.handle = win32gui.FindWindow(None, client_title)
        self.inner_handles = getInnnerWindows(self.handle) if self.handle else []
        self.inner_handle = self.inner_handles[0] if self.inner_handles else None
        self.ipc = IPC()

        if not self.handle or not self.inner_handle:
            print(f"Window '{client_title}' not found or inner window not found.")
            self.handle = None
            self.inner_handle = None
        else:
            print(f"Found window handles: {self.handle}, {self.inner_handle}")
            self.tracker = WindowTracker(
                self.inner_handle, self.handle, self.on_size_changed, interval=1.0
            )
            self.tracker.start()

    async def on_size_changed(self, inner_size, outer_size, reference_size):
        message_data = {"inner_size": inner_size, "outer_size": outer_size}
        self.ipc.publish(MessageType.SIZE_CHANGE, message_data)

    def setMainUI(self, main_ui):
        self.main_ui = main_ui

    def stop(self):
        if self.tracker:
            self.tracker.stop()
