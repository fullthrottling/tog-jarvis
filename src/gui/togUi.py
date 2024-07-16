from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QStatusBar
from .topMenu import TopMenu
from src.gui.centerLayout import CenterLayout


class TogJarvisUI(QMainWindow):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.setupUi()

    def start(self):
        self.show()
        self.client.setMainUI(self)

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

        # 상태바 추가
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def onStart(self):
        self.center_layout.onStart()
        self.status_bar.showMessage("Started")

    def onTestFunction(self):
        self.center_layout.onTestFunction()
        self.status_bar.showMessage("Test function executed")

    def onCheckSize(self):
        self.center_layout.onCheckSize()
        self.status_bar.showMessage("Size checked")

    def onMouseTracer(self):
        self.center_layout.onMouseTracer()
        if self.top_menu.actionMouseTracer.isChecked():
            self.status_bar.showMessage("Mouse tracing activated")
        else:
            self.status_bar.showMessage("Mouse tracing deactivated")

    def onCapture(self):
        self.center_layout.onCapture()
        self.status_bar.showMessage("Capture taken")

    # 상태바 메시지를 업데이트하는 메서드 추가
    def updateStatusBar(self, message):
        self.status_bar.showMessage(message)
