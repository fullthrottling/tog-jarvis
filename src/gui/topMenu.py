from PySide6.QtWidgets import QMenuBar, QMenu
from PySide6.QtGui import QAction


class TopMenu(QMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setupMenus()

    def setupMenus(self):
        self.menu = self.addMenu("메뉴")
        self.menu_2 = self.addMenu("설정")
        self.menu_3 = self.addMenu("보기")
        self.menu_4 = self.addMenu("개발")

        self.menuvaaadsd = QMenu("슈퍼", self.menu)
        self.menu.addMenu(self.menuvaaadsd)

        self.actionDebug = QAction("Debug", self, checkable=True)
        self.actionTest = QAction("Test", self, checkable=True)
        self.actionCheckSise = QAction("Check Size", self)
        self.actionMouseTracer = QAction("MouseTracer", self, checkable=True)
        self.actionCapture = QAction("Capture", self)

        self.menuvaaadsd.addAction(self.actionTest)
        self.menu_4.addAction(self.actionDebug)
        self.menu_4.addAction(self.actionCheckSise)
        self.menu_4.addAction(self.actionMouseTracer)
        self.menu_4.addAction(self.actionCapture)

        self.actionTest.toggled.connect(self.parent.onTestFunction)
        self.actionCheckSise.triggered.connect(self.parent.onCheckSize)
        self.actionMouseTracer.triggered.connect(self.parent.onMouseTracer)
        self.actionCapture.triggered.connect(self.parent.onCapture)
