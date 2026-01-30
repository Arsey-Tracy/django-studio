from PySide6.QtWidgets import (
    QTextEdit
)


class LogWidget(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setStyleSheet("background-color: #1E1E1E; color: #00FF00; font-family: Consolas;")
        self.setPlaceholderText("Django Server Logs will appear here...")