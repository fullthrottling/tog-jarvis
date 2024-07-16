import sys
import os
import asyncio
import traceback
from PySide6.QtWidgets import QApplication
from src.gui.togUi import TogJarvisUI
from src.client.client import Client
from qasync import QEventLoop


async def main():
    def close_future(future, loop):
        loop.call_later(10, future.cancel)
        future.cancel()

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    if hasattr(app, "aboutToQuit"):
        getattr(app, "aboutToQuit").connect(lambda: close_future(future, loop))

    try:
        client = Client()
    except Exception as e:
        print(f"Error initializing Client: {e}")
        return

    main_window = TogJarvisUI(client)
    main_window.show()

    await future


if __name__ == "__main__":
    try:
        qapp = QApplication(sys.argv)
        loop = QEventLoop(qapp)
        asyncio.set_event_loop(loop)
        future = asyncio.Future()

        with loop:
            loop.run_until_complete(main())
    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
