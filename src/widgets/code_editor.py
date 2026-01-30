from PySide6.QtGui import (
    QColor, QFont, QTextCursor, QTextFormat, QPainter, QKeySequence
)
from PySide6.QtWidgets import QTextEdit
from PySide6.QtCore import Qt, QRect, Signal

from ui.syntax_highlighter import PythonHighlighter
from widgets.line_number_area import LineNumberArea
from utils.code_folder import CodeFolder
from utils.python_formatter import PythonFormatter
from utils.bracket_matcher import BracketMatcher
from utils.git_gutter import GitGutter
from utils.multi_cursor import MultiCursor
from theme.django_theme import DjangoTheme


class CodeEditor(QTextEdit):
    """The Main Editor Widget with Auto-Indent, Find & Replace, Code Folding, and Auto-Format"""
    
    find_requested = Signal()
    dirty_changed = Signal(bool)  # Emitted when dirty state changes
    save_requested = Signal()  # Emitted when Ctrl+S is pressed
    
    def __init__(self):
        super().__init__()
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.lineNumberArea = LineNumberArea(self)
        self.find_widget = None  # Will be set by parent
        
        # Dirty state tracking
        self.is_dirty = False
        self.file_path = None
        
        # Code folding
        self.foldable_regions = []  # List of (start_line, end_line, type)
        self.folded_regions = set()  # Set of folded line numbers
        
        # Bracket matching
        self.bracket_positions = None  # Tuple of (open_pos, close_pos) or None
        
        # Git gutter
        self.git_changes = {}  # Dict of line_num: change_type
        
        # Multi-cursor
        self.multi_cursor = MultiCursor()
        self.multi_cursor_enabled = False
        
        # Editor Visuals
        self.setFont(QFont("Consolas", 11))
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {DjangoTheme.TERTIARY_BG}; 
                color: {DjangoTheme.TEXT_PRIMARY}; 
                border: none;
            }}
        """)
        
        # Connect signals
        self.document().blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.verticalScrollBar().valueChanged.connect(self.updateLineNumberArea)
        self.textChanged.connect(self.on_text_changed)  # Modified to track dirty state
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.cursorPositionChanged.connect(self.updateLineNumberArea)
        
        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()
        
        # Attach Syntax Highlighter
        self.highlighter = PythonHighlighter(self.document())
        
        # Update foldable regions on text change
        self.textChanged.connect(self.update_foldable_regions)
    
    def on_text_changed(self):
        """Handle text changes and track dirty state"""
        self.updateLineNumberArea()
        if not self.is_dirty:
            self.set_dirty(True)
    
    def set_dirty(self, dirty: bool):
        """Set the dirty state of the editor"""
        if self.is_dirty != dirty:
            self.is_dirty = dirty
            self.dirty_changed.emit(dirty)
    
    def set_file_path(self, path: str):
        """Set the file path associated with this editor"""
        self.file_path = path
    
    def get_file_path(self) -> str:
        """Get the file path associated with this editor"""
        return self.file_path if self.file_path else ""

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
        painter.fillRect(event.rect(), QColor(DjangoTheme.SECONDARY_BG))

        block = self.document().begin()
        blockNumber = 0
        top = int(self.document().documentLayout().blockBoundingRect(block).top())
        top -= self.verticalScrollBar().value()
        height = self.fontMetrics().height()

        while block.isValid():
            bottom = top + int(self.document().documentLayout().blockBoundingRect(block).height())
            if block.isVisible() and bottom >= event.rect().top() and top <= event.rect().bottom():
                number = str(blockNumber + 1)
                painter.setPen(QColor(DjangoTheme.TEXT_SECONDARY))
                painter.drawText(0, top, self.lineNumberArea.width() - 25, height, Qt.AlignRight, number)
                
                # Draw git gutter indicator if this line has changes
                if blockNumber in self.git_changes:
                    change_type = self.git_changes[blockNumber]
                    if change_type == 'added':
                        color = QColor(DjangoTheme.STATUS_SUCCESS)  # Green for added
                    elif change_type == 'modified':
                        color = QColor(DjangoTheme.STATUS_INFO)  # Blue for modified
                    elif change_type == 'deleted':
                        color = QColor(DjangoTheme.STATUS_ERROR)  # Red for deleted
                    else:
                        color = QColor(DjangoTheme.STATUS_WARNING)  # Gold for other
                    
                    painter.fillRect(self.lineNumberArea.width() - 5, top, 4, height, color)
                
                # Draw fold indicator if this line is foldable
                if self.is_line_foldable(blockNumber):
                    fold_marker = "−" if blockNumber in self.folded_regions else "+"
                    fold_color = QColor(DjangoTheme.ACCENT_PRIMARY) if blockNumber in self.folded_regions else QColor(DjangoTheme.TEXT_MUTED)
                    painter.setPen(fold_color)
                    painter.setFont(QFont("Consolas", 10, QFont.Bold))
                    painter.drawText(self.lineNumberArea.width() - 20, top, 18, height, Qt.AlignCenter, fold_marker)

            block = block.next()
            top = bottom
            blockNumber += 1

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(DjangoTheme.DJANGO_GREEN_ACCENT)
            lineColor.setAlpha(30)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        
        # Add bracket matching highlights
        self._add_bracket_highlights(extraSelections)
        
        self.setExtraSelections(extraSelections)
    
    def _add_bracket_highlights(self, selections: list):
        """Add bracket pair highlighting"""
        cursor = self.textCursor()
        text = self.toPlainText()
        pos = cursor.positionInBlock() if cursor.block().isValid() else 0
        
        # Find matching brackets
        match_result = BracketMatcher.find_matching_bracket(text, pos)
        if not match_result:
            self.bracket_positions = None
            return
        
        bracket_pos, match_pos = match_result
        self.bracket_positions = (bracket_pos, match_pos)
        
        # Highlight opening bracket with Django green
        selection1 = QTextEdit.ExtraSelection()
        selection1.format.setBackground(QColor(DjangoTheme.ACCENT_PRIMARY))
        selection1.format.setForeground(QColor(DjangoTheme.PRIMARY_BG))
        selection1.cursor = QTextCursor(self.document())
        selection1.cursor.setPosition(bracket_pos)
        selection1.cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
        selections.append(selection1)
        
        # Highlight closing bracket with Django green
        selection2 = QTextEdit.ExtraSelection()
        selection2.format.setBackground(QColor(DjangoTheme.ACCENT_PRIMARY))
        selection2.format.setForeground(QColor(DjangoTheme.PRIMARY_BG))
        selection2.cursor = QTextCursor(self.document())
        selection2.cursor.setPosition(match_pos)
        selection2.cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
        selections.append(selection2)

    def keyPressEvent(self, event):
        """Handle Auto-Indentation, Smart Backspace, Find/Replace shortcuts, and Save"""
        # Ctrl+S: Save file
        if event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            self.save_requested.emit()
            return
        
        # Ctrl+F: Open Find
        if event.key() == Qt.Key_F and event.modifiers() == Qt.ControlModifier:
            self.find_requested.emit()
            return
        
        # Ctrl+H: Open Replace
        if event.key() == Qt.Key_H and event.modifiers() == Qt.ControlModifier:
            self.find_requested.emit()
            if self.find_widget:
                self.find_widget.replace_input.setFocus()
            return
        
        # Return: Auto-indent
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
            
        # Backspace: Smart dedent
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
    
    def update_foldable_regions(self):
        """Update foldable code regions"""
        code = self.toPlainText()
        self.foldable_regions = CodeFolder.find_foldable_regions(code)
        self.updateLineNumberArea()
    
    def get_foldable_region_for_line(self, line_num: int):
        """Get foldable region that starts at given line"""
        for start, end, region_type in self.foldable_regions:
            if start == line_num:
                return (start, end, region_type)
        return None
    
    def is_line_foldable(self, line_num: int) -> bool:
        """Check if a line has a foldable region"""
        return self.get_foldable_region_for_line(line_num) is not None
    
    def toggle_fold(self, line_num: int):
        """Toggle folding for a specific line"""
        region = self.get_foldable_region_for_line(line_num)
        if not region:
            return
        
        start, end, region_type = region
        
        if line_num in self.folded_regions:
            # Unfold
            self.folded_regions.discard(line_num)
            self.show_lines(start + 1, end)
        else:
            # Fold
            self.folded_regions.add(line_num)
            self.hide_lines(start + 1, end)
        
        self.updateLineNumberArea()
    
    def hide_lines(self, start: int, end: int):
        """Hide lines from start to end (inclusive)"""
        doc = self.document()
        cursor = QTextCursor(doc)
        
        for line_num in range(start, end + 1):
            block = doc.findBlockByLineNumber(line_num)
            if block.isValid():
                block.setVisible(False)
    
    def show_lines(self, start: int, end: int):
        """Show lines from start to end (inclusive)"""
        doc = self.document()
        
        for line_num in range(start, end + 1):
            block = doc.findBlockByLineNumber(line_num)
            if block.isValid():
                block.setVisible(True)
    
    def format_code_on_save(self):
        """Auto-format code before saving"""
        current_code = self.toPlainText()
        formatted_code = PythonFormatter.format_code(current_code)
        
        # Only update if formatting changed anything
        if formatted_code != current_code:
            cursor = self.textCursor()
            cursor_pos = cursor.position()
            
            self.setPlainText(formatted_code)
            
            # Try to restore cursor position
            if cursor_pos <= len(formatted_code):
                cursor.setPosition(cursor_pos)
                self.setTextCursor(cursor)
    
    def update_git_gutter(self):
        """Update git gutter information"""
        if self.file_path:
            self.git_changes = GitGutter.get_changed_lines(self.file_path)
            self.updateLineNumberArea()
    
    def toggle_multi_cursor(self):
        """Toggle multi-cursor mode"""
        self.multi_cursor_enabled = not self.multi_cursor_enabled
        if not self.multi_cursor_enabled:
            self.multi_cursor.clear()
        return self.multi_cursor_enabled
    
    def add_cursor_at_position(self, pos: int):
        """Add additional cursor at position"""
        if self.multi_cursor_enabled:
            cursor = QTextCursor(self.document())
            cursor.setPosition(pos)
            self.multi_cursor.add_cursor(cursor)
    
    def get_all_cursor_positions(self) -> list:
        """Get all cursor positions in multi-cursor mode"""
        if self.multi_cursor_enabled:
            return [c.positionInBlock() for c in self.multi_cursor]
        return [self.textCursor().positionInBlock()]