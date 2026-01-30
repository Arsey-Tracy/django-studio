"""Breadcrumb navigation widget"""
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from utils.breadcrumb import Breadcrumb


class BreadcrumbWidget(QWidget):
    """Shows code navigation breadcrumb trail"""
    
    line_selected = Signal(int)  # Emitted when breadcrumb item clicked
    
    def __init__(self, editor=None, parent=None):
        super().__init__(parent)
        self.editor = editor
        self.breadcrumbs = []
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(8, 4, 8, 4)
        self.layout.setSpacing(0)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #2D2D30;
                border-bottom: 1px solid #333333;
            }
            QPushButton {
                background-color: transparent;
                color: #A0A0A0;
                border: none;
                padding: 2px 4px;
                font-size: 11px;
                text-align: left;
            }
            QPushButton:hover {
                color: #D4D4D4;
                background-color: #3E3E42;
            }
        """)
        
        # Connect editor signals
        if editor:
            editor.cursorPositionChanged.connect(self.update_breadcrumb)
            editor.textChanged.connect(self.update_breadcrumb)
    
    def update_breadcrumb(self):
        """Update breadcrumb based on cursor position"""
        if not self.editor:
            return
        
        # Get cursor line
        cursor = self.editor.textCursor()
        line = cursor.blockNumber()
        
        # Get breadcrumb
        code = self.editor.toPlainText()
        breadcrumb = Breadcrumb.get_breadcrumb(code, line)
        
        # Update UI
        self._refresh_breadcrumb(breadcrumb)
    
    def _refresh_breadcrumb(self, breadcrumb):
        """Refresh breadcrumb UI"""
        # Clear old buttons
        while self.layout.count() > 0:
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.breadcrumbs = breadcrumb
        
        # Add breadcrumb buttons
        for i, (name, line_num) in enumerate(breadcrumb):
            if name == 'file':
                label = QLabel('📄 file')
                label.setStyleSheet("color: #A0A0A0; padding: 2px 4px; font-size: 11px;")
                self.layout.addWidget(label)
            else:
                btn = QPushButton(name)
                btn.setFlat(True)
                btn.setFont(QFont("Segoe UI", 10))
                btn.clicked.connect(lambda checked, line=line_num: self.line_selected.emit(line))
                self.layout.addWidget(btn)
            
            # Add separator (except for last item)
            if i < len(breadcrumb) - 1:
                sep = QLabel('›')
                sep.setStyleSheet("color: #666666; padding: 0px 4px; font-size: 11px;")
                self.layout.addWidget(sep)
        
        # Add stretch
        self.layout.addStretch()
    
    def set_editor(self, editor):
        """Set the editor to track"""
        self.editor = editor
        if editor:
            editor.cursorPositionChanged.connect(self.update_breadcrumb)
            editor.textChanged.connect(self.update_breadcrumb)
