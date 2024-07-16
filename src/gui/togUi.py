import win32gui
import win32api
import win32process
import ctypes
import time
import threading
from src.window_manager.window_tracker import WindowTracker
from src.common.utils import getInnnerWindows
from src.window_manager.window_utils import calculate_relative_coordinates
from src.common.togConfig import TogConfig

user32 = ctypes.windll.user32


class Client:
    def __init__(self):
        self.config = TogConfig()
        self.handle = win32gui.FindWindow(None, self.config.client_tile)
        self.inner_handles = getInnnerWindows(self.handle) if self.handle else []
        self.inner_handle = self.inner_handles[0] if self.inner_handles else None

        self.reference_size = (
            self.config.reference_width,
            self.config.reference_height,
        )

        if not self.handle:
            raise Exception(f"Window '{self.config.client_tile}' not found.")

        if not self.inner_handle:
            raise Exception(f"Inner window for '{self.config.client_tile}' not found.")

        print(f"Found window handles: {self.handle}, {self.inner_handle}")
        self.tracker = WindowTracker(
            self.inner_handle,
            self.handle,
            self.on_size_changed,
            interval=1.0,
            reference_size=self.reference_size,
        )
        self.tracker.start()

    def setupWindowSize(self):
        if self.handle:
            try:
                self.force_set_foreground(self.handle)
            except Exception as e:
                print(f"Failed to set foreground window: {e}")

    def force_set_foreground(self, hwnd):
        try:
            fg_window = win32gui.GetForegroundWindow()
            fg_thread = win32process.GetWindowThreadProcessId(fg_window)[0]
            current_thread = win32api.GetCurrentThreadId()
            if fg_thread != current_thread:
                user32.AttachThreadInput(fg_thread, current_thread, True)
                win32gui.SetForegroundWindow(hwnd)
                user32.AttachThreadInput(fg_thread, current_thread, False)
            else:
                win32gui.SetForegroundWindow(hwnd)
        except Exception as e:
            print(f"Failed to force set foreground: {e}")

    def on_size_changed(self, inner_size, outer_size, reference_size):
        inner_width, inner_height = inner_size
        outer_width, outer_height = outer_size
        print(f"Inner window size changed to {inner_width}x{inner_height}")
        print(f"Outer window size changed to {outer_width}x{outer_height}")

        x, y = 100, 100
        new_inner_x, new_inner_y = calculate_relative_coordinates(
            reference_size, inner_size, x, y
        )
        print(f"New inner coordinates: {new_inner_x}, {new_inner_y}")

        new_outer_x, new_outer_y = calculate_relative_coordinates(
            reference_size, outer_size, x, y
        )
        print(f"New outer coordinates: {new_outer_x}, {new_outer_y}")

    def stop(self):
        if self.tracker:
            self.tracker.stop()
