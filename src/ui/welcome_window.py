import os
from PySide6.QtCore import Signal, QSettings, Qt
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QMessageBox, QVBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QPushButton, QFileDialog
)
from PySide6.QtGui import QFont
from theme.django_theme import DjangoTheme

class WelcomeWindow(QWidget):
    project_selected = Signal(str)      
    request_new_project = Signal()      

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚀 Django Studio - Welcome")
        self.resize(1000, 700)
        self.setStyleSheet(f"""
            QWidget {{ 
                background-color: {DjangoTheme.PRIMARY_BG}; 
                color: {DjangoTheme.TEXT_PRIMARY}; 
                font-family: Segoe UI, sans-serif; 
            }}
            QLabel {{ 
                color: {DjangoTheme.TEXT_PRIMARY}; 
            }}
            QListWidget {{ 
                background-color: {DjangoTheme.SECONDARY_BG}; 
                border: 1px solid {DjangoTheme.BORDER_COLOR}; 
                border-radius: 4px;
                font-size: 12px; 
            }}
            QListWidget::item {{ 
                padding: 12px; 
                border-bottom: 1px solid {DjangoTheme.BORDER_COLOR}; 
                color: {DjangoTheme.TEXT_PRIMARY};
            }}
            QListWidget::item:hover {{ 
                background-color: {DjangoTheme.DJANGO_GREEN_ACCENT}; 
            }}
            QPushButton {{ 
                background-color: {DjangoTheme.DJANGO_GREEN}; 
                color: white;
                border: none; 
                border-radius: 6px; 
                padding: 16px 20px; 
                font-size: 14px;
                font-weight: bold;
                text-align: left;
            }}
            QPushButton:hover {{ 
                background-color: {DjangoTheme.ACCENT_PRIMARY}; 
            }}
            QPushButton:pressed {{
                background-color: {DjangoTheme.DJANGO_GREEN_LIGHT};
            }}
        """)

        self.settings = QSettings("DjangoStudio", "RecentProjects")
        self.recents = self.settings.value("paths", []) or [] 

        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Left Panel
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        recent_label = QLabel("Recent Projects")
        recent_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        recent_label.setStyleSheet(f"color: {DjangoTheme.TEXT_PRIMARY};")
        left_layout.addWidget(recent_label)
        
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
                item.setText(f"📁 {name}\n{path}") 
                item.setData(Qt.UserRole, path) 
                self.recent_list.addItem(item)
                
        left_layout.addWidget(self.recent_list)

        # Right Panel
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignTop)
        right_layout.setSpacing(20)

        logo = QLabel("🚀 Django Studio")
        logo.setFont(QFont("Segoe UI", 36, QFont.Bold))
        logo.setStyleSheet(f"color: {DjangoTheme.ACCENT_PRIMARY}; margin-bottom: 10px;")
        right_layout.addWidget(logo)
        
        tagline = QLabel("Professional Django Development Environment")
        tagline.setFont(QFont("Segoe UI", 12))
        tagline.setStyleSheet(f"color: {DjangoTheme.TEXT_SECONDARY}; margin-bottom: 30px;")
        right_layout.addWidget(tagline)

        btn_new = QPushButton("✨  Create New Project\n    Start a fresh Django setup")
        btn_new.setMinimumHeight(80)
        btn_new.clicked.connect(self.request_new_project.emit)
        right_layout.addWidget(btn_new)

        btn_open = QPushButton("📂  Open Existing Project\n    Browse your computer")
        btn_open.setMinimumHeight(80)
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
