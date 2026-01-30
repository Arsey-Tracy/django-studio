"""Minimap widget for code editor visualization"""
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtGui import QPainter, QColor, QFont, QTextCursor
from PySide6.QtCore import Qt, QRect, Signal, QSize
from theme.django_theme import DjangoTheme


class Minimap(QWidget):
    """Code minimap showing overview of entire file"""
    
    clicked = Signal(int)  # Emitted with line number when clicked
    
    def __init__(self, editor, parent=None):
        super().__init__(parent)
        self.editor = editor
        self.setFixedWidth(140)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {DjangoTheme.SECONDARY_BG};
                border-left: 2px solid {DjangoTheme.BORDER_COLOR};
            }}
        """)
        
        # Connect editor signals
        self.editor.textChanged.connect(self.update)
        self.editor.verticalScrollBar().valueChanged.connect(self.update)
        self.editor.cursorPositionChanged.connect(self.update)
    
    def sizeHint(self) -> QSize:
        return QSize(140, self.editor.height())
    
    def paintEvent(self, event):
        """Paint the minimap"""
        painter = QPainter(self)
        painter.fillRect(event.rect(), QColor(DjangoTheme.SECONDARY_BG))
        
        doc = self.editor.document()
        if not doc or doc.blockCount() == 0:
            painter.end()
            return
        
        total_lines = doc.blockCount()
        widget_height = self.height()
        line_height = max(1, widget_height / total_lines)
        
        # Draw all lines
        for block_num in range(total_lines):
            block = doc.findBlockByLineNumber(block_num)
            if not block.isValid():
                continue
            
            text = block.text().strip()
            if not text:
                continue
            
            # Get color based on syntax (simple heuristic)
            color = self._get_line_color(text)
            
            # Draw line representation
            y = int(block_num * line_height)
            height = max(1, int(line_height))
            
            painter.fillRect(0, y, self.width() - 4, height, color)
        
        # Draw viewport indicator (which part is visible)
        self._draw_viewport_indicator(painter, total_lines, line_height)
        # Painter end is called in _draw_viewport_indicator
    
    def _get_line_color(self, text: str) -> QColor:
        """Determine line color based on content - Django themed"""
        if text.startswith('def ') or text.startswith('class '):
            return QColor(DjangoTheme.ACCENT_PRIMARY)  # Django green for definitions
        elif text.startswith('import ') or text.startswith('from '):
            return QColor(DjangoTheme.ACCENT_SECONDARY)  # Orange for imports
        elif text.startswith('#'):
            return QColor(DjangoTheme.TEXT_MUTED)  # Muted for comments
        elif 'return' in text or 'if ' in text or 'for ' in text:
            return QColor(DjangoTheme.STATUS_INFO)  # Blue for keywords
        else:
            return QColor(DjangoTheme.TEXT_SECONDARY)  # Secondary text for regular code
    
    def _draw_viewport_indicator(self, painter: QPainter, total_lines: int, line_height: float):
        """Draw the visible viewport indicator"""
        if total_lines == 0:
            painter.end()
            return
        
        try:
            # Get viewport range
            visible_blocks = self.editor.document().blockCount()
            
            # Use textCursor to get block number, not cursorRect
            cursor = self.editor.textCursor()
            first_block = cursor.blockNumber() if cursor.hasSelection() or not cursor.atBlockStart() else 0
            viewport_height = self.editor.height() / max(1, self.editor.fontMetrics().lineSpacing())
            
            viewport_start = max(0, first_block - 2)
            viewport_end = min(visible_blocks - 1, first_block + int(viewport_height) + 2)
            
            # Draw semi-transparent viewport indicator with Django green
            y_start = (viewport_start / visible_blocks) * self.height()
            y_end = (viewport_end / visible_blocks) * self.height()
            height = max(2, y_end - y_start)
            
            viewport_color = QColor(DjangoTheme.ACCENT_PRIMARY)
            viewport_color.setAlpha(80)
            painter.fillRect(0, int(y_start), self.width(), int(height), viewport_color)
        except Exception:
            pass  # Silently ignore errors during viewport drawing
        finally:
            painter.end()  # Always end the painter
        painter.drawRect(0, int(y_start), self.width() - 1, int(height) - 1, QColor(0, 122, 204, 150))
    
    def mousePressEvent(self, event):
        """Handle clicks to jump to location"""
        total_lines = self.editor.document().blockCount()
        if total_lines == 0:
            return
        
        # Calculate which line was clicked
        line_num = int((event.y() / self.height()) * total_lines)
        line_num = max(0, min(line_num, total_lines - 1))
        
        # Move cursor to that line
        self.clicked.emit(line_num)
        
        # Jump to line in editor
        block = self.editor.document().findBlockByLineNumber(line_num)
        cursor = QTextCursor(block)
        self.editor.setTextCursor(cursor)
        self.editor.ensureCursorVisible()
    
    def mouseMoveEvent(self, event):
        """Smooth scrolling while dragging"""
        if event.buttons() & Qt.LeftButton:
            self.mousePressEvent(event)
