from src.ipc.message_types import MessageType


class IPCHandler:
    def __init__(self, ipc, ui):
        self.ipc = ipc
        self.ui = ui
        self.ipc.subscribe(MessageType.SIZE_CHANGE, self.handle_size_change)
        self.ipc.subscribe(MessageType.STATUS_UPDATE, self.handle_status_update)
        self.ipc.subscribe(MessageType.ERROR, self.handle_error)

    def handle_size_change(self, data):
        self.ui.update_status_signal.emit(
            f"Inner: {data['inner_size']}, Outer: {data['outer_size']}"
        )

    def handle_status_update(self, data):
        self.ui.update_status_signal.emit(f"Status: {data['status']}")

    def handle_error(self, data):
        self.ui.update_status_signal.emit(f"Error: {data['error']}")
