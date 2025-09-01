from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel
)

class ProjectWizard(QWidget):
    def __init__(self):
        super().__init__()
        self.set_ui()
    def set_ui(self):
        layout = QVBoxLayout(self)
        header = QLabel("Django Project Wizard")
        layout.addWidget(header)