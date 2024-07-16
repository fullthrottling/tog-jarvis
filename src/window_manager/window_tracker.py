import ctypes
import ctypes.wintypes as wintypes
import asyncio
import time
import threading


class WindowTracker:
    def __init__(self, inner_hwnd, outer_hwnd, callback, interval=1.0):
        self.inner_hwnd = inner_hwnd
        self.outer_hwnd = outer_hwnd
        self.callback = callback
        self.interval = interval
        self.running = False
        self.thread = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def _run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._track_window_size(loop))

    async def _track_window_size(self, loop):
        while self.running:
            inner_size = self._get_window_size(self.inner_hwnd)
            outer_size = self._get_window_size(self.outer_hwnd)
            reference_size = (800, 600)  # 임의의 참조 크기 설정
            await self.callback(inner_size, outer_size, reference_size)
            await asyncio.sleep(self.interval)

    def _get_window_size(self, hwnd):
        rect = wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
        width = rect.right - rect.left
        height = rect.bottom - rect.top
        return (width, height)
