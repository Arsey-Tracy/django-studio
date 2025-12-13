from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QSize

class LineNumberArea(QWidget):
    """The side gutter that paints line numbers"""
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)
