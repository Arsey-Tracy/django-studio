import os
from PySide6.QtCore import QProcess, Signal, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QStackedWidget, QLineEdit, QLabel, QListWidget,
    QPushButton, QProgressBar, QMessageBox, QHBoxLayout, QCheckBox
)

class ProjectWizard(QWidget):
    project_ready = Signal(str) 

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Django Studio - New Project")
        self.resize(600, 450)
        self.setStyleSheet("""
            QWidget { background-color: #2D2D30; color: #CCCCCC; font-family: Segoe UI, sans-serif; }
            QLineEdit { background-color: #3E3E42; border: 1px solid #555; padding: 5px; color: white; }
            QPushButton { background-color: #0E639C; color: white; border: none; padding: 8px; font-weight: bold; }
            QPushButton:disabled { background-color: #555; color: #888; }
            QPushButton:hover { background-color: #1177BB; }
            QListWidget { background-color: #1E1E1E; border: 1px solid #555; }
            QProgressBar { border: 2px solid grey; border-radius: 5px; text-align: center; }
            QProgressBar::chunk { background-color: #0E639C; width: 20px; }
        """)

        self.main_layout = QVBoxLayout(self)
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)

        self.current_project_path = ""
        self.python_exec = "python" 

        self.init_project_page()
        self.init_apps_page()

    # --- Page 1: Create Project ---
    def init_project_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Create New Django Project")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        layout.addWidget(title)

        self.project_input = QLineEdit()
        self.project_input.setPlaceholderText("Enter Project Name (e.g., my_saas)")
        self.project_input.textChanged.connect(self.validate_project_form)
        layout.addWidget(self.project_input)

        self.project_loader = QProgressBar()
        self.project_loader.setRange(0, 0)
        self.project_loader.hide()
        layout.addWidget(self.project_loader)

        self.create_btn = QPushButton("Create Project")
        self.create_btn.setEnabled(False)
        self.create_btn.clicked.connect(self.run_create_project)
        layout.addWidget(self.create_btn)

        self.stack.addWidget(page)

    def validate_project_form(self):
        text = self.project_input.text().strip()
        self.create_btn.setEnabled(len(text) > 0)

    def run_create_project(self):
        project_name = self.project_input.text().strip()
        self.project_input.setEnabled(False)
        self.create_btn.hide()
        self.project_loader.show()
        
        self.proc = QProcess(self)
        self.proc.finished.connect(self.on_project_created)
        # Use -m django startproject to ensure we use the python env's django
        self.proc.start(self.python_exec, ["-m", "django", "startproject", project_name])

    def on_project_created(self, exit_code, exit_status):
        if exit_code == 0:
            project_name = self.project_input.text().strip()
            self.current_project_path = os.path.abspath(project_name)
            self.project_created_label.setText(f"Project '{project_name}' Created Successfully!")
            self.stack.setCurrentIndex(1) 
        else:
            err = self.proc.readAllStandardError().data().decode()
            QMessageBox.critical(self, "Error", f"Failed to create project:\n{err}")
            self.project_input.setEnabled(True)
            self.create_btn.show()
            self.project_loader.hide()

    # --- Page 2: Create Apps ---
    def init_apps_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(10)

        self.project_created_label = QLabel("Project Created!")
        self.project_created_label.setStyleSheet("color: #4EC9B0; font-weight: bold;")
        layout.addWidget(self.project_created_label)

        form_layout = QHBoxLayout()
        self.app_input = QLineEdit()
        self.app_input.setPlaceholderText("App Name (e.g., users)")
        self.app_input.textChanged.connect(self.validate_app_form)
        
        self.add_app_btn = QPushButton("Add App")
        self.add_app_btn.setEnabled(False)
        self.add_app_btn.setFixedWidth(100)
        self.add_app_btn.clicked.connect(self.run_create_app)
        
        form_layout.addWidget(self.app_input)
        form_layout.addWidget(self.add_app_btn)
        layout.addLayout(form_layout)

        self.multi_app_toggle = QCheckBox("Create Multiple Apps")
        self.multi_app_toggle.setChecked(True) 
        layout.addWidget(self.multi_app_toggle)

        self.app_loader = QProgressBar()
        self.app_loader.setRange(0, 0)
        self.app_loader.setFixedHeight(5) 
        self.app_loader.hide()
        layout.addWidget(self.app_loader)

        layout.addWidget(QLabel("Created Apps:"))
        self.apps_list = QListWidget()
        layout.addWidget(self.apps_list)

        self.finish_btn = QPushButton("Finish & Open Studio")
        self.finish_btn.setStyleSheet("background-color: #4EC9B0; color: black;")
        self.finish_btn.clicked.connect(self.emit_project_ready)
        layout.addWidget(self.finish_btn)

        self.stack.addWidget(page)

    def validate_app_form(self):
        text = self.app_input.text().strip()
        self.add_app_btn.setEnabled(len(text) > 0)

    def run_create_app(self):
        app_name = self.app_input.text().strip()
        self.app_input.setEnabled(False)
        self.add_app_btn.setEnabled(False)
        self.app_loader.show()

        self.app_proc = QProcess(self)
        self.app_proc.setWorkingDirectory(self.current_project_path)
        self.app_proc.finished.connect(lambda: self.on_app_created(app_name))
        self.app_proc.start(self.python_exec, ["manage.py", "startapp", app_name])

    def on_app_created(self, app_name):
        self.apps_list.addItem(f"✔ {app_name}")
        self.app_loader.hide()
        self.app_input.setEnabled(True)
        self.app_input.setFocus()
        
        if self.multi_app_toggle.isChecked():
            self.app_input.clear()
            self.add_app_btn.setEnabled(False)
        else:
            self.app_input.clear()

    def emit_project_ready(self):
        if not self.current_project_path:
            self.close()
            return
        self.project_ready.emit(self.current_project_path)
        self.close()
