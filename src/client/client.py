import win32gui
import win32api
import win32process
import ctypes
import asyncio
from src.common.togConfig import TogConfig
from src.window_manager.window_tracker import WindowTracker
from src.common.utils import getInnnerWindows
from src.ipc.ipc import IPC
from PySide6.QtCore import QMetaObject, Qt, Q_ARG, QObject

user32 = ctypes.windll.user32


class Client(QObject):
    def __init__(self):
        super().__init__()
        self.togConfig = TogConfig()
        client_tile = self.togConfig.configJson.client_title
        self.handle = win32gui.FindWindow(None, client_tile)
        self.inner_handles = getInnnerWindows(self.handle) if self.handle else []
        self.inner_handle = self.inner_handles[0] if self.inner_handles else None
        self.ipc = IPC()

        if not self.handle or not self.inner_handle:
            print(f"Window '{client_tile}' not found or inner window not found.")
            self.handle = None
            self.inner_handle = None
        else:
            print(f"Found window handles: {self.handle}, {self.inner_handle}")
            self.tracker = WindowTracker(
                self.inner_handle, self.handle, self.on_size_changed, interval=1.0
            )
            self.tracker.start()

    async def on_size_changed(self, inner_size, outer_size, reference_size):
        inner_width, inner_height = inner_size
        outer_width, outer_height = outer_size
        message = {
            "inner_size": (inner_width, inner_height),
            "outer_size": (outer_width, outer_height),
        }
        await self.ipc.send(message)
        await self.update_gui(message)

    async def update_gui(self, message):
        inner_size = message["inner_size"]
        outer_size = message["outer_size"]
        QMetaObject.invokeMethod(
            self.main_ui,
            "updateStatusBar",
            Qt.QueuedConnection,
            Q_ARG(str, f"Inner: {inner_size}, Outer: {outer_size}"),
        )

    def setMainUI(self, main_ui):
        self.main_ui = main_ui

    def stop(self):
        if self.tracker:
            self.tracker.stop()
