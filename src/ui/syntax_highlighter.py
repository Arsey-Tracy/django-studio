import re
from PySide6.QtGui import (
    QTextCharFormat, QColor, QFont, QSyntaxHighlighter
)


class PythonHighlighter(QSyntaxHighlighter):
    """Enhanced RegEx-based Python Syntax Highlighter with Django theme colors"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._mapping = {}

        # === Colors (Django Theme) ===
        base_fmt = QTextCharFormat()
        base_fmt.setForeground(QColor("#E8EEF5"))  # Django light text
        
        # Keywords (Django green, bold)
        keyword_fmt = QTextCharFormat()
        keyword_fmt.setForeground(QColor("#44B78B"))
        keyword_fmt.setFontWeight(QFont.Bold)
        
        # Strings (Orange accent)
        string_fmt = QTextCharFormat()
        string_fmt.setForeground(QColor("#FF9E64"))
        
        # Comments (Muted text)
        comment_fmt = QTextCharFormat()
        comment_fmt.setForeground(QColor("#7A8895"))
        
        # Class/Type names (Django light green)
        class_fmt = QTextCharFormat()
        class_fmt.setForeground(QColor("#44B78B"))
        
        # Numbers (Light blue)
        number_fmt = QTextCharFormat()
        number_fmt.setForeground(QColor("#0C90FF"))
        
        # Operators (Secondary text)
        operator_fmt = QTextCharFormat()
        operator_fmt.setForeground(QColor("#A8B5C4"))
        
        # Built-in functions (Django light green)
        builtin_fmt = QTextCharFormat()
        builtin_fmt.setForeground(QColor("#44B78B"))
        
        # Decorators (Orange)
        decorator_fmt = QTextCharFormat()
        decorator_fmt.setForeground(QColor("#FF9E64"))
        
        # === 1. Comments (must be first to avoid interference) ===
        self._mapping[r"#[^\n]*"] = comment_fmt
        
        # === 2. F-Strings and Regular Strings ===
        # F-strings with content highlighting
        self._mapping[r'f"(?:\\.|[^"\\])*"'] = string_fmt
        self._mapping[r"f'(?:\\.|[^'\\])*'"] = string_fmt
        # Triple-quoted strings
        self._mapping[r'"""(?:\\.|[^\\])*?"""'] = string_fmt
        self._mapping[r"'''(?:\\.|[^\\])*?'''"] = string_fmt
        # Regular strings
        self._mapping[r'"(?:\\.|[^"\\])*"'] = string_fmt
        self._mapping[r"'(?:\\.|[^'\\])*'"] = string_fmt
        
        # === 3. Decorators ===
        self._mapping[r"@[a-zA-Z_][a-zA-Z0-9_]*"] = decorator_fmt
        
        # === 4. Keywords ===
        keywords = [
            "def", "class", "if", "else", "elif", "return", "import", 
            "from", "try", "except", "finally", "while", "for", "in", "not", "and", "or",
            "None", "True", "False", "pass", "break", "continue", "lambda", "with", "as",
            "yield", "assert", "del", "global", "nonlocal", "raise", "is"
        ]
        for word in keywords:
            self._mapping[rf"\b{word}\b"] = keyword_fmt
        
        # === 5. Built-in Functions ===
        builtins = [
            "print", "len", "str", "int", "float", "bool", "list", "dict", "set", "tuple",
            "range", "enumerate", "zip", "map", "filter", "sum", "min", "max", "abs",
            "round", "sorted", "reversed", "isinstance", "issubclass", "callable", "hasattr",
            "getattr", "setattr", "delattr", "type", "open", "input", "eval", "exec",
            "compile", "repr", "ascii", "format", "hex", "oct", "bin", "ord", "chr",
            "vars", "dir", "help", "id", "hash", "all", "any", "super", "property"
        ]
        for builtin in builtins:
            self._mapping[rf"\b{builtin}\b"] = builtin_fmt
        
        # === 6. Numbers (integers, floats, hex, binary, octal) ===
        # Hex numbers: 0x...
        self._mapping[r"\b0[xX][0-9a-fA-F]+\b"] = number_fmt
        # Binary numbers: 0b...
        self._mapping[r"\b0[bB][01]+\b"] = number_fmt
        # Octal numbers: 0o...
        self._mapping[r"\b0[oO][0-7]+\b"] = number_fmt
        # Float numbers: 1.23, .5, 1e-10
        self._mapping[r"\b\d+\.?\d*([eE][+-]?\d+)?\b"] = number_fmt
        # Regular integers
        self._mapping[r"\b\d+\b"] = number_fmt
        
        # === 7. Operators ===
        # Multi-char operators first
        self._mapping[r"(==|!=|<=|>=|<<|>>|//|\*\*|->|=>)"] = operator_fmt
        # Single-char operators
        self._mapping[r"[+\-*/%=<>!&|^~]"] = operator_fmt
        
        # === 8. Class/Type names (PascalCase) ===
        self._mapping[r"\b[A-Z][a-zA-Z0-9_]*\b"] = class_fmt

    def highlightBlock(self, text):
        """Apply all formatting patterns to the text block"""
        for pattern, fmt in self._mapping.items():
            for match in re.finditer(pattern, text):
                self.setFormat(match.start(), match.end() - match.start(), fmt)
