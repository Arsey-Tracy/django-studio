from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QMouseEvent

class LineNumberArea(QWidget):
    """The side gutter that paints line numbers and handles code folding"""
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)
    
    def mousePressEvent(self, event: QMouseEvent):
        """Handle fold/unfold clicks in the gutter"""
        # Check if click is in the fold marker area (rightmost part of line number area)
        if event.x() > self.width() - 25:
            # Get line number from click position
            cursor = self.editor.cursorForPosition(event.pos())
            line_num = cursor.blockNumber()
            
            # Toggle fold for this line
            if self.editor.is_line_foldable(line_num):
                self.editor.toggle_fold(line_num)
        
        super().mousePressEvent(event)
