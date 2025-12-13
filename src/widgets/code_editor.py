from PySide6.QtGui import (
    QColor, QFont, QTextCursor, QTextFormat, QPainter
)
from PySide6.QtWidgets import QTextEdit
from PySide6.QtCore import Qt, QRect

from ui.syntax_highlighter import PythonHighlighter
from widgets.line_number_area import LineNumberArea


class CodeEditor(QTextEdit):
    """The Main Editor Widget with Auto-Indent"""
    def __init__(self):
        super().__init__()
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.lineNumberArea = LineNumberArea(self)
        
        # Editor Visuals
        self.setFont(QFont("Consolas", 11))
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E; 
                color: #D4D4D4; 
                border: none;
            }
        """)
        
        # Connect signals
        self.document().blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.verticalScrollBar().valueChanged.connect(self.updateLineNumberArea)
        self.textChanged.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.cursorPositionChanged.connect(self.updateLineNumberArea)
        
        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()
        
        # Attach Syntax Highlighter
        self.highlighter = PythonHighlighter(self.document())

    def lineNumberAreaWidth(self):
        digits = len(str(max(1, self.document().blockCount())))
        space = 25 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _=None):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, _=None):
        self.lineNumberArea.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor("#252526"))

        block = self.document().begin()
        blockNumber = 0
        top = int(self.document().documentLayout().blockBoundingRect(block).top())
        top -= self.verticalScrollBar().value()
        height = self.fontMetrics().height()

        while block.isValid():
            bottom = top + int(self.document().documentLayout().blockBoundingRect(block).height())
            if block.isVisible() and bottom >= event.rect().top() and top <= event.rect().bottom():
                number = str(blockNumber + 1)
                painter.setPen(QColor("#858585"))
                painter.drawText(0, top, self.lineNumberArea.width() - 5, height, Qt.AlignRight, number)

            block = block.next()
            top = bottom
            blockNumber += 1

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor("#2D2D30")
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def keyPressEvent(self, event):
        """Handle Auto-Indentation and Smart Backspace"""
        if event.key() == Qt.Key_Return:
            cursor = self.textCursor()
            block = cursor.block()
            text = block.text()
            
            # 1. Calculate indent
            leading_space = ""
            for char in text:
                if char in (" ", "\t"):
                    leading_space += char
                else:
                    break
            
            # 2. Check for increase (:)
            stripped_text = text.rstrip()
            if stripped_text.endswith(":"):
                indentation = leading_space + "    " 
            else:
                indentation = leading_space 

            # 3. Insert
            cursor.insertText("\n" + indentation)
            self.setTextCursor(cursor)
            return
            
        elif event.key() == Qt.Key_Backspace:
            cursor = self.textCursor()
            if cursor.atBlockStart():
                block = cursor.block().previous()
                if block.isValid():
                    text = block.text()
                    if text.startswith("    "): # Check for 4 spaces
                        cursor.movePosition(QTextCursor.StartOfBlock)
                        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 4)
                        if cursor.selectedText().isspace():
                            cursor.removeSelectedText()
                            return 
                            
        super().keyPressEvent(event)