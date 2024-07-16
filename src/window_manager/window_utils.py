import win32gui
import win32process
import psutil


def get_window_handle(app_name):
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            try:
                process = psutil.Process(pid)
                if process.name().lower() == app_name.lower():
                    hwnds.append(hwnd)
            except psutil.NoSuchProcess:
                pass
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds[0] if hwnds else None


def calculate_relative_coordinates(reference_size, current_size, x, y):
    ref_width, ref_height = reference_size
    cur_width, cur_height = current_size

    relative_x = x * (cur_width / ref_width)
    relative_y = y * (cur_height / ref_height)

    return int(relative_x), int(relative_y)


def get_window_rect(hwnd):
    return win32gui.GetWindowRect(hwnd)
