from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QTextEdit

class Editor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.font = QFontDatabase("Courier New")
        self.setFont(self.font)