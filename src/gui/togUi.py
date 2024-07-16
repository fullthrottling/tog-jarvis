from PySide6.QtWidgets import QMainWindow, QStatusBar, QWidget, QVBoxLayout
from PySide6.QtCore import Signal, Slot
from .topMenu import TopMenu
from .centerLayout import CenterLayout
from src.ipc.ipc_handler import IPCHandler


class TogJarvisUI(QMainWindow):
    update_status_signal = Signal(str)

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.ipc = client.ipc
        self.client.setMainUI(self)
        self.handler = IPCHandler(self.ipc, self)
        self.setupUi()

        self.update_status_signal.connect(self.updateStatusBar)

    def setupUi(self):
        self.setWindowTitle("Tog-Jarvis")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.top_menu = TopMenu(self)
        self.setMenuBar(self.top_menu)

        self.center_layout = CenterLayout(self)
        main_layout.addWidget(self.center_layout)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    @Slot(str)
    def updateStatusBar(self, message: str):
        self.status_bar.showMessage(message)

    def onTestFunction(self):
        print("Test function triggered")

    def onCheckSize(self):
        print("Check size triggered")

    def onMouseTracer(self):
        print("Mouse tracer triggered")

    def onCapture(self):
        print("Capture triggered")
