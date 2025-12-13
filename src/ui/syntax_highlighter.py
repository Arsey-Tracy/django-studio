import re
from PySide6.QtGui import (
    QTextCharFormat, QColor, QFont, QSyntaxHighlighter
)


class PythonHighlighter(QSyntaxHighlighter):
    """RegEx-based Python Syntax Highlighter"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._mapping = {}

        # Colors (VS Code Dark Theme inspired)
        base_fmt = QTextCharFormat()
        base_fmt.setForeground(QColor("#D4D4D4"))
        
        keyword_fmt = QTextCharFormat()
        keyword_fmt.setForeground(QColor("#569CD6")) # Blue
        keyword_fmt.setFontWeight(QFont.Bold)
        
        string_fmt = QTextCharFormat()
        string_fmt.setForeground(QColor("#CE9178")) # Orange
        
        comment_fmt = QTextCharFormat()
        comment_fmt.setForeground(QColor("#6A9955")) # Green
        
        class_fmt = QTextCharFormat()
        class_fmt.setForeground(QColor("#4EC9B0")) # Teal
        
        # 1. Keywords
        keywords = ["def", "class", "if", "else", "elif", "return", "import", 
                   "from", "try", "except", "while", "for", "in", "None", "True", "False",
                   "pass", "break", "continue", "lambda", "with", "as"]
        for word in keywords:
            self._mapping[rf"\b{word}\b"] = keyword_fmt

        # 2. Strings
        self._mapping[r'".*"'] = string_fmt
        self._mapping[r"'.*'"] = string_fmt
        
        # 3. Comments
        self._mapping[r"#[^\n]*"] = comment_fmt
        
        # 4. Class/Function names (heuristic)
        self._mapping[r"\b[A-Z][a-zA-Z0-9_]+\b"] = class_fmt

    def highlightBlock(self, text):
        for pattern, fmt in self._mapping.items():
            for match in re.finditer(pattern, text):
                self.setFormat(match.start(), match.end() - match.start(), fmt)
