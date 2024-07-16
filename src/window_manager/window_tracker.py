import win32gui
import time
import threading


class WindowTracker:
    def __init__(
        self, inner_hwnd, outer_hwnd, callback, interval=1.0, reference_size=(800, 600)
    ):
        self.inner_hwnd = inner_hwnd
        self.outer_hwnd = outer_hwnd
        self.callback = callback
        self.interval = interval
        self.running = False
        self.thread = None
        self.last_inner_size = self.get_window_size(self.inner_hwnd)
        self.last_outer_size = self.get_window_size(self.outer_hwnd)
        self.reference_size = reference_size  # 기준 크기

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run)
            self.thread.daemon = True
            self.thread.start()
            print(
                f"Started tracking window size for hwnd: {self.inner_hwnd}, {self.outer_hwnd}"
            )

    def stop(self):
        if self.running:
            self.running = False
            if self.thread is not None:
                self.thread.join()
            print(
                f"Stopped tracking window size for hwnd: {self.inner_hwnd}, {self.outer_hwnd}"
            )

    def _run(self):
        while self.running:
            current_inner_size = self.get_window_size(self.inner_hwnd)
            current_outer_size = self.get_window_size(self.outer_hwnd)
            if (
                current_inner_size != self.last_inner_size
                or current_outer_size != self.last_outer_size
            ):
                self.last_inner_size = current_inner_size
                self.last_outer_size = current_outer_size
                self.callback(
                    current_inner_size, current_outer_size, self.reference_size
                )
            time.sleep(self.interval)

    def get_window_size(self, hwnd):
        rect = win32gui.GetClientRect(hwnd)
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]
        return width, height
