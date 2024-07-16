import asyncio


class IPC:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def send(self, message):
        await self.queue.put(message)

    async def receive(self):
        return await self.queue.get()
