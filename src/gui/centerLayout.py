from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QTextBrowser,
    QScrollArea,
)
from PySide6.QtCore import QRect
from qasync import asyncSlot
import asyncio
from src.common.utils import captureImage


class CenterLayout(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setupUi()

    def setupUi(self):
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setGeometry(QRect(30, 10, 511, 781))
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 509, 779))

        self.textBrowser = QTextBrowser(self.scrollAreaWidgetContents)
        self.textBrowser.setGeometry(QRect(0, 0, 511, 781))

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(QRect(90, 830, 75, 24))
        self.pushButton.setText("Start")
        self.pushButton.clicked.connect(self.onStart)

        self.label = QLabel(self)
        self.label.setGeometry(QRect(280, 810, 191, 41))
        self.label.setText("TextLabel")

    def onStart(self):
        self.textBrowser.append("onStart")
        print("onStart")

    def onTestFunction(self):
        self.textBrowser.append("onTestFunction")
        print("onTestFunction")

    def onCheckSize(self):
        inner, outer = self.parent.client.getClientSize()
        self.textBrowser.append(f"Inner: {inner} Outer: {outer}")

    def onMouseTracer(self):
        @asyncSlot()
        async def on_mouse_tracer(self):
            while self.parent.top_menu.actionMouseTracer.isChecked():
                inner, outer = self.parent.client.getCurrentMousePosition()
                self.label.setText(f"Inner: {inner} Outer: {outer}")
                await asyncio.sleep(0.1)

    def onCapture(self):
        @asyncSlot()
        async def onCapture(self):
            try:
                inner, outer = self.parent.client.getClientSize()
                await captureImage(
                    self.parent.client.handle,
                    "./temp/",
                    "outer.png",
                    0,
                    0,
                    outer[0],
                    outer[1],
                )
                await captureImage(
                    self.parent.client.innerHandle,
                    "./temp/",
                    "inner.png",
                    0,
                    0,
                    inner[0],
                    inner[1],
                )
            except Exception as e:
                print(e)
