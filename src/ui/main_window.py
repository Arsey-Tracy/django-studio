from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileSystemModel, QTreeView, QSplitter,  QMessageBox,
    QTabWidget, QTextEdit, QLabel, QStyle, QToolBar
)
from PySide6.QtCore import Qt, QDir, QSize, QFileInfo, QProcess
from PySide6.QtGui import QAction
from widgets.api_tester_widget import APITesterWidget
from widgets.code_editor import CodeEditor
                           
class DjangoStudioWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Django Studio")
        self.resize(1200, 800)
        self.setStyleSheet("background-color: #333333; color: white;")
        
        self.open_files = {} 
        self.current_project_path = ""
        self.server_process = None

        self.setup_ui()
        self.setup_toolbar()

    def setup_ui(self):
        # Main Splitter
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Left: Project Tree
        self.project_tree = QTreeView()
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath()) 
        self.project_tree.setModel(self.file_model)
        self.project_tree.hideColumn(1)
        self.project_tree.hideColumn(2)
        self.project_tree.hideColumn(3)
        self.project_tree.setHeaderHidden(True)
        self.project_tree.setStyleSheet("""
            QTreeView { background-color: #252526; color: #CCCCCC; border: none; }
            QTreeView::item:hover { background-color: #2A2D2E; }
            QTreeView::item:selected { background-color: #37373D; color: white; }
        """)
        self.project_tree.doubleClicked.connect(self.open_file_from_tree)
        
        # Right: Editor + Logs/API
        right_splitter = QSplitter(Qt.Vertical)
        
        # 1. Editor Tabs
        self.editor_tabs = QTabWidget()
        self.editor_tabs.setTabsClosable(True)
        self.editor_tabs.setDocumentMode(True)
        self.editor_tabs.setStyleSheet("""
            QTabWidget::pane { border: 0; }
            QTabBar::tab { background: #2D2D30; color: #969696; padding: 8px 15px; }
            QTabBar::tab:selected { background: #1E1E1E; color: white; border-top: 2px solid #007ACC; }
        """)
        self.editor_tabs.tabCloseRequested.connect(self.close_tab)
        
        # 2. South Panel (Logs + API Tester)
        self.south_tabs = QTabWidget()
        self.south_tabs.setStyleSheet("""
            QTabWidget::pane { border: 0; }
            QTabBar::tab { background: #333333; color: #969696; padding: 5px 10px; }
            QTabBar::tab:selected { background: #1E1E1E; color: white; }
        """)

        # Tab 1: Terminal/Log
        self.log_widget = QTextEdit()
        self.log_widget.setReadOnly(True)
        self.log_widget.setStyleSheet("background-color: #1E1E1E; color: #00FF00; font-family: Consolas;")
        self.log_widget.setPlaceholderText("Django Server Logs will appear here...")

        # Tab 2: API Tester
        self.api_tester = APITesterWidget()

        self.south_tabs.addTab(self.log_widget, "Terminal / Logs")
        self.south_tabs.addTab(self.api_tester, "API Tester")

        right_splitter.addWidget(self.editor_tabs)
        right_splitter.addWidget(self.south_tabs)
        right_splitter.setStretchFactor(0, 4)
        right_splitter.setStretchFactor(1, 1)

        main_splitter.addWidget(self.project_tree)
        main_splitter.addWidget(right_splitter)
        main_splitter.setStretchFactor(0, 1) 
        main_splitter.setStretchFactor(1, 5)
        
        self.setCentralWidget(main_splitter)

    def setup_toolbar(self):
        toolbar = QToolBar("Django Controls")
        toolbar.setIconSize(QSize(20, 20))
        toolbar.setMovable(False)
        toolbar.setStyleSheet("QToolBar { background-color: #333333; border-bottom: 1px solid #444; spacing: 10px; padding: 5px; }")
        self.addToolBar(toolbar)

        def add_action(name, icon_type, method):
            icon = self.style().standardIcon(icon_type)
            action = QAction(icon, name, self)
            action.triggered.connect(method)
            toolbar.addAction(action)
            return action

        # Server Group
        toolbar.addWidget(QLabel("  SERVER: "))
        self.act_run = add_action("Run Server", QStyle.SP_MediaPlay, self.run_dev_server)
        self.act_stop = add_action("Stop Server", QStyle.SP_MediaStop, self.stop_dev_server)
        self.act_stop.setEnabled(False)
        
        toolbar.addSeparator()

        # Database Group
        toolbar.addWidget(QLabel("  DB: "))
        add_action("Make Migrations", QStyle.SP_FileIcon, self.make_migrations)
        add_action("Migrate", QStyle.SP_DialogApplyButton, self.run_migrate)

        toolbar.addSeparator()

        # Utils
        toolbar.addWidget(QLabel("  UTILS: "))
        add_action("New App", QStyle.SP_FileDialogNewFolder, self.open_new_app_dialog)

    # --- Actions ---
    def run_dev_server(self):
        if not self.current_project_path:
            QMessageBox.warning(self, "No Project", "Please open a project first.")
            return

        self.log_widget.append("\n--- Starting Django Server ---")
        self.south_tabs.setCurrentIndex(0) # Show Log Tab
        
        self.server_process = QProcess(self)
        self.server_process.setWorkingDirectory(self.current_project_path)
        self.server_process.readyReadStandardOutput.connect(self.handle_server_output)
        self.server_process.readyReadStandardError.connect(self.handle_server_error)
        
        self.server_process.start("python", ["manage.py", "runserver"])
        
        # Update API Tester URL
        self.api_tester.set_server_context("http://127.0.0.1:8000/")
        
        self.act_run.setEnabled(False)
        self.act_stop.setEnabled(True)

    def stop_dev_server(self):
        if self.server_process and self.server_process.state() == QProcess.Running:
            self.server_process.terminate()
            self.log_widget.append("--- Server Stopped ---")
            self.api_tester.set_server_context("Server Offline")
            self.act_run.setEnabled(True)
            self.act_stop.setEnabled(False)

    def handle_server_output(self):
        data = self.server_process.readAllStandardOutput().data().decode()
        self.log_widget.insertPlainText(data)
        self.log_widget.ensureCursorVisible()

    def handle_server_error(self):
        data = self.server_process.readAllStandardError().data().decode()
        self.log_widget.insertPlainText(data)
        self.log_widget.ensureCursorVisible()

    def make_migrations(self):
        self.log_widget.append("Running: makemigrations... (Implementation Pending)")
    
    def run_migrate(self):
        self.log_widget.append("Running: migrate... (Implementation Pending)")

    def open_new_app_dialog(self):
        QMessageBox.information(self, "New App", "Open Wizard to add apps.")

    # --- File System ---
    def set_project_path(self, path):
        self.current_project_path = path
        self.file_model.setRootPath(path)
        index = self.file_model.index(path)
        self.project_tree.setRootIndex(index)

    def close_tab(self, index):
        widget = self.editor_tabs.widget(index)
        for path, idx in list(self.open_files.items()):
            if idx == index:
                del self.open_files[path]
                break
        widget.deleteLater()
        self.editor_tabs.removeTab(index)

    def open_file_from_tree(self, index):
        file_path = self.file_model.filePath(index)
        if self.file_model.isDir(index): return

        if file_path in self.open_files:
            self.editor_tabs.setCurrentIndex(self.open_files[file_path])
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                new_editor = CodeEditor()
                new_editor.setPlainText(content)
                file_name = QFileInfo(file_path).fileName()
                new_index = self.editor_tabs.addTab(new_editor, file_name)
                self.editor_tabs.setCurrentIndex(new_index)
                self.open_files[file_path] = new_index
        except Exception as e:
            self.log_widget.append(f"Error opening file: {e}")
