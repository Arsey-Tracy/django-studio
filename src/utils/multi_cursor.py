"""Multi-cursor support for text editor"""
from typing import List, Set
from PySide6.QtGui import QTextCursor


class MultiCursor:
    """Manages multiple cursor positions"""
    
    def __init__(self):
        self.cursors: List[QTextCursor] = []
        self.primary_cursor_index = 0
    
    def add_cursor(self, cursor: QTextCursor):
        """Add a cursor to the multi-cursor set"""
        self.cursors.append(cursor)
    
    def clear(self):
        """Clear all cursors"""
        self.cursors.clear()
        self.primary_cursor_index = 0
    
    def get_primary_cursor(self) -> QTextCursor:
        """Get the primary cursor"""
        if 0 <= self.primary_cursor_index < len(self.cursors):
            return self.cursors[self.primary_cursor_index]
        return None
    
    def set_primary_cursor(self, index: int):
        """Set which cursor is primary"""
        if 0 <= index < len(self.cursors):
            self.primary_cursor_index = index
    
    def insert_text_at_all(self, text: str) -> List[QTextCursor]:
        """Insert text at all cursor positions"""
        updated_cursors = []
        for cursor in self.cursors:
            cursor.insertText(text)
            updated_cursors.append(cursor)
        return updated_cursors
    
    def select_word_at_all(self) -> List[QTextCursor]:
        """Select word at all cursor positions"""
        selected = []
        for cursor in self.cursors:
            cursor.select(QTextCursor.WordUnderCursor)
            selected.append(cursor)
        return selected
    
    def delete_at_all(self) -> List[QTextCursor]:
        """Delete character at all cursor positions"""
        deleted = []
        for cursor in self.cursors:
            cursor.deleteChar()
            deleted.append(cursor)
        return deleted
    
    def __len__(self):
        return len(self.cursors)
    
    def __iter__(self):
        return iter(self.cursors)
