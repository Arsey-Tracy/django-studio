from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, 
    QLabel, QCheckBox, QFrame
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QIcon, QTextCursor, QTextDocument
from theme.django_theme import DjangoTheme


class FindReplaceWidget(QWidget):
    """Find & Replace toolbar widget for code editor"""
    
    close_requested = Signal()
    
    def __init__(self, editor=None, parent=None):
        super().__init__(parent)
        self.editor = editor
        self.current_match_index = -1
        self.matches = []
        
        self.init_ui()
        self.setup_styles()
        
    def init_ui(self):
        """Build the Find & Replace UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # --- Find Row ---
        find_layout = QHBoxLayout()
        
        find_label = QLabel("Find:")
        find_label.setMinimumWidth(50)
        
        self.find_input = QLineEdit()
        self.find_input.setPlaceholderText("Search text...")
        self.find_input.textChanged.connect(self.on_find_text_changed)
        self.find_input.returnPressed.connect(self.find_next)
        
        self.case_sensitive = QCheckBox("Case")
        self.case_sensitive.toggled.connect(self.on_find_text_changed)
        
        self.whole_word = QCheckBox("Whole Word")
        self.whole_word.toggled.connect(self.on_find_text_changed)
        
        self.find_prev_btn = QPushButton("◀ Prev")
        self.find_prev_btn.setMaximumWidth(80)
        self.find_prev_btn.clicked.connect(self.find_prev)
        
        self.find_next_btn = QPushButton("Next ▶")
        self.find_next_btn.setMaximumWidth(80)
        self.find_next_btn.clicked.connect(self.find_next)
        
        self.close_btn = QPushButton("✕")
        self.close_btn.setMaximumWidth(40)
        self.close_btn.clicked.connect(self.close_requested.emit)
        
        find_layout.addWidget(find_label)
        find_layout.addWidget(self.find_input, 1)
        find_layout.addWidget(self.case_sensitive)
        find_layout.addWidget(self.whole_word)
        find_layout.addWidget(self.find_prev_btn)
        find_layout.addWidget(self.find_next_btn)
        find_layout.addWidget(self.close_btn)
        
        main_layout.addLayout(find_layout)
        
        # --- Replace Row ---
        replace_layout = QHBoxLayout()
        
        replace_label = QLabel("Replace:")
        replace_label.setMinimumWidth(50)
        
        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("Replacement text...")
        self.replace_input.returnPressed.connect(self.replace_next)
        
        self.replace_btn = QPushButton("Replace")
        self.replace_btn.setMaximumWidth(100)
        self.replace_btn.clicked.connect(self.replace_next)
        
        self.replace_all_btn = QPushButton("Replace All")
        self.replace_all_btn.setMaximumWidth(100)
        self.replace_all_btn.clicked.connect(self.replace_all)
        
        self.match_count = QLabel("No matches")
        self.match_count.setStyleSheet(f"color: {DjangoTheme.TEXT_SECONDARY}; font-size: 12px;")
        
        replace_layout.addWidget(replace_label)
        replace_layout.addWidget(self.replace_input, 1)
        replace_layout.addWidget(self.replace_btn)
        replace_layout.addWidget(self.replace_all_btn)
        replace_layout.addWidget(self.match_count)
        
        main_layout.addLayout(replace_layout)
    
    def setup_styles(self):
        """Apply Django theme styling"""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {DjangoTheme.SECONDARY_BG};
                color: {DjangoTheme.TEXT_PRIMARY};
            }}
            QLineEdit {{
                background-color: {DjangoTheme.TERTIARY_BG};
                border: 1px solid {DjangoTheme.BORDER_COLOR};
                border-radius: 4px;
                padding: 6px;
                color: {DjangoTheme.TEXT_PRIMARY};
                selection-background-color: {DjangoTheme.ACCENT_PRIMARY};
            }}
            QLineEdit:focus {{
                border: 2px solid {DjangoTheme.ACCENT_PRIMARY};
            }}
            QPushButton {{
                background-color: {DjangoTheme.DJANGO_GREEN};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 14px;
                font-weight: bold;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {DjangoTheme.ACCENT_PRIMARY};
            }}
            QPushButton:pressed {{
                background-color: {DjangoTheme.DJANGO_GREEN_LIGHT};
            }}
            QCheckBox {{
                spacing: 6px;
                color: {DjangoTheme.TEXT_PRIMARY};
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
            }}
            QCheckBox::indicator:unchecked {{
                background-color: {DjangoTheme.TERTIARY_BG};
                border: 2px solid {DjangoTheme.BORDER_COLOR};
                border-radius: 2px;
            }}
            QCheckBox::indicator:checked {{
                background-color: {DjangoTheme.ACCENT_PRIMARY};
                border: 2px solid {DjangoTheme.ACCENT_PRIMARY};
                border-radius: 2px;
            }}
            QLabel {{
                color: {DjangoTheme.TEXT_PRIMARY};
            }}
        """)
    
    def on_find_text_changed(self):
        """Handle find text input changes"""
        self.current_match_index = -1
        self.update_matches()
        if self.matches:
            self.find_next()
        else:
            self.match_count.setText("No matches")
    
    def update_matches(self):
        """Find all matches in the document"""
        if not self.editor:
            return
        
        self.matches = []
        search_text = self.find_input.text()
        
        if not search_text:
            self.match_count.setText("No matches")
            return
        
        flags = QTextDocument.FindFlag(0)
        if self.case_sensitive.isChecked():
            flags |= QTextDocument.FindCaseSensitively
        if self.whole_word.isChecked():
            flags |= QTextDocument.FindWholeWords
        
        cursor = QTextCursor(self.editor.document())
        cursor.movePosition(QTextCursor.Start)
        
        while not cursor.isNull():
            cursor = self.editor.document().find(search_text, cursor, flags)
            if not cursor.isNull():
                self.matches.append(cursor.blockNumber())
                cursor.movePosition(QTextCursor.EndOfWord)
        
        count = len(self.matches)
        self.match_count.setText(f"{count} match{'es' if count != 1 else ''}")
    
    def find_next(self):
        """Find and highlight next occurrence"""
        if not self.editor or not self.matches:
            return
        
        self.current_match_index = (self.current_match_index + 1) % len(self.matches)
        self.highlight_match(self.current_match_index)
    
    def find_prev(self):
        """Find and highlight previous occurrence"""
        if not self.editor or not self.matches:
            return
        
        self.current_match_index = (self.current_match_index - 1) % len(self.matches)
        self.highlight_match(self.current_match_index)
    
    def highlight_match(self, match_index):
        """Highlight a specific match and scroll to it"""
        if not self.editor or match_index >= len(self.matches):
            return
        
        line_number = self.matches[match_index]
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.Start)
        cursor.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor, line_number)
        
        # Find and select the text on this line
        search_text = self.find_input.text()
        flags = QTextDocument.FindFlag(0)
        if self.case_sensitive.isChecked():
            flags |= QTextDocument.FindCaseSensitively
        
        start_pos = cursor.positionInBlock()
        line_cursor = QTextCursor(self.editor.document().findBlock(cursor.position()))
        line_cursor.movePosition(QTextCursor.StartOfBlock)
        line_cursor = self.editor.document().find(search_text, line_cursor, flags)
        
        if not line_cursor.isNull():
            self.editor.setTextCursor(line_cursor)
            self.editor.ensureCursorVisible()
    
    def replace_next(self):
        """Replace the current match and move to next"""
        if not self.editor or not self.find_input.text():
            return
        
        cursor = self.editor.textCursor()
        selected = cursor.selectedText()
        find_text = self.find_input.text()
        replace_text = self.replace_input.text()
        
        # If current selection matches search text, replace it
        if selected == find_text or (not self.case_sensitive.isChecked() and selected.lower() == find_text.lower()):
            cursor.insertText(replace_text)
            self.editor.setTextCursor(cursor)
        
        # Move to next match
        self.update_matches()
        if self.matches:
            self.find_next()
    
    def replace_all(self):
        """Replace all occurrences"""
        if not self.editor or not self.find_input.text():
            return
        
        find_text = self.find_input.text()
        replace_text = self.replace_input.text()
        
        flags = QTextDocument.FindFlag(0)
        if self.case_sensitive.isChecked():
            flags |= QTextDocument.FindCaseSensitively
        if self.whole_word.isChecked():
            flags |= QTextDocument.FindWholeWords
        
        cursor = QTextCursor(self.editor.document())
        cursor.movePosition(QTextCursor.Start)
        
        replaced_count = 0
        while not cursor.isNull():
            cursor = self.editor.document().find(find_text, cursor, flags)
            if not cursor.isNull():
                cursor.insertText(replace_text)
                replaced_count += 1
            else:
                break
        
        self.match_count.setText(f"Replaced {replaced_count} occurrence{'s' if replaced_count != 1 else ''}")
        self.update_matches()
    
    def set_editor(self, editor):
        """Set the editor widget to search in"""
        self.editor = editor
    
    def focus_find_input(self):
        """Focus the find input and select all text"""
        self.find_input.setFocus()
        self.find_input.selectAll()
