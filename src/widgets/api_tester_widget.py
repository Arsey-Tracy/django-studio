from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLineEdit, QPushButton,
    QGroupBox, QPlainTextEdit
)
from PySide6.QtGui import QFont

class APITesterWidget(QWidget):
    """Standalone API Tester Integration"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QWidget { background-color: #1E1E1E; color: #D4D4D4; }
            QLineEdit, QComboBox, QPlainTextEdit { 
                background-color: #2D2D30; border: 1px solid #3E3E42; padding: 4px; color: white;
            }
            QGroupBox { border: 1px solid #3E3E42; margin-top: 6px; padding-top: 10px; font-weight: bold;}
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px; }
        """)
        layout = QVBoxLayout(self)
        
        # --- Top Bar ---
        top_bar = QHBoxLayout()
        self.method_combo = QComboBox()
        self.method_combo.addItems(["GET", "POST", "PUT", "PATCH", "DELETE"])
        self.method_combo.setFixedWidth(80)
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter API Endpoint...")
        
        self.send_button = QPushButton("Send Request")
        self.send_button.setStyleSheet("background-color: #4EC9B0; color: black; font-weight: bold; padding: 5px;")
        self.send_button.clicked.connect(self.execute_request)
        
        top_bar.addWidget(self.method_combo)
        top_bar.addWidget(self.url_input)
        top_bar.addWidget(self.send_button)
        layout.addLayout(top_bar)
        
        # --- Body Input ---
        self.body_input = QGroupBox("Request Body (JSON)")
        body_layout = QVBoxLayout(self.body_input)
        self.json_editor = QPlainTextEdit()
        self.json_editor.setPlaceholderText('{\n  "key": "value"\n}')
        self.json_editor.setFont(QFont("Consolas", 10))
        body_layout.addWidget(self.json_editor)
        layout.addWidget(self.body_input)
        
        # --- Response Output ---
        self.response_output = QGroupBox("Response")
        response_layout = QVBoxLayout(self.response_output)
        self.response_text = QPlainTextEdit()
        self.response_text.setReadOnly(True)
        self.response_text.setPlaceholderText("Response data will appear here...")
        self.response_text.setFont(QFont("Consolas", 10))
        response_layout.addWidget(self.response_text)
        layout.addWidget(self.response_output)
        
        # Context
        self.set_server_context("http://127.0.0.1:8000/")

    def set_server_context(self, base_url):
        self.url_input.setText(base_url)
        
    def execute_request(self):
        # Placeholder for actual HTTP logic
        method = self.method_combo.currentText()
        url = self.url_input.text()
        self.response_text.setPlainText(f"Sending {method} request to {url}...\n\n[Integration Pending: Connect 'requests' library here]")

