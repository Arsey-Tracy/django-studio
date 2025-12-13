import os
from PySide6.QtCore import Signal, QSettings, Qt
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QMessageBox, QVBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QFileDialog
)
class WelcomeWindow(QWidget):
    project_selected = Signal(str)      
    request_new_project = Signal()      

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to Django Studio")
        self.resize(800, 600)
        self.setStyleSheet("""
            QWidget { background-color: #2D2D30; color: white; font-family: Segoe UI, sans-serif; }
            QLabel { font-size: 24px; font-weight: bold; color: #CCCCCC; }
            QListWidget { background-color: #1E1E1E; border: none; font-size: 14px; }
            QListWidget::item { padding: 10px; border-bottom: 1px solid #333; }
            QListWidget::item:hover { background-color: #2A2D2E; }
            QPushButton { 
                background-color: #333333; border: 1px solid #444; border-radius: 8px; 
                padding: 15px; font-size: 16px; text-align: left;
            }
            QPushButton:hover { background-color: #3E3E42; border: 1px solid #007ACC; }
        """)

        self.settings = QSettings("DjangoStudio", "RecentProjects")
        self.recents = self.settings.value("paths", []) or [] 

        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        
        # Left Panel
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(QLabel("Recent Projects"))
        
        self.recent_list = QListWidget()
        self.recent_list.setFocusPolicy(Qt.NoFocus) 
        self.recent_list.itemClicked.connect(self.open_recent)
        
        if not self.recents:
            self.recent_list.addItem("No recent projects found.")
            self.recent_list.setEnabled(False)
        else:
            for path in self.recents:
                item = QListWidgetItem()
                name = os.path.basename(path)
                item.setText(f"{name}\n{path}") 
                item.setData(Qt.UserRole, path) 
                self.recent_list.addItem(item)
                
        left_layout.addWidget(self.recent_list)

        # Right Panel
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignTop)
        right_layout.setSpacing(20)

        logo = QLabel("Django Studio")
        logo.setStyleSheet("font-size: 32px; color: #4EC9B0; margin-bottom: 20px;")
        right_layout.addWidget(logo)

        btn_new = QPushButton("✚  Create New Project\n    Start a fresh Django setup")
        btn_new.clicked.connect(self.request_new_project.emit)
        right_layout.addWidget(btn_new)

        btn_open = QPushButton("📂  Open Existing Project\n    Browse your computer")
        btn_open.clicked.connect(self.browse_project)
        right_layout.addWidget(btn_open)

        main_layout.addWidget(left_panel, 2)
        main_layout.addWidget(right_panel, 1)

    def browse_project(self):
        folder = QFileDialog.getExistingDirectory(self, "Open Django Project")
        if folder:
            self.add_to_recents(folder)
            self.project_selected.emit(folder)

    def open_recent(self, item):
        path = item.data(Qt.UserRole)
        if path and os.path.exists(path):
            self.add_to_recents(path) 
            self.project_selected.emit(path)
        else:
            QMessageBox.warning(self, "Error", "Project path no longer exists.")

    def add_to_recents(self, path):
        if path in self.recents:
            self.recents.remove(path)
        self.recents.insert(0, path)
        self.recents = self.recents[:10] 
        self.settings.setValue("paths", self.recents)
