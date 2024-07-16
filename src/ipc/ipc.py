class IPC:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, message_type, callback):
        if message_type not in self.subscribers:
            self.subscribers[message_type] = []
        self.subscribers[message_type].append(callback)

    def publish(self, message_type, data):
        if message_type in self.subscribers:
            for callback in self.subscribers[message_type]:
                callback(data)
