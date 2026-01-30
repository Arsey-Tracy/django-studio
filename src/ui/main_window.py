from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileSystemModel, QTreeView, QSplitter,  QMessageBox,
    QTabWidget, QTextEdit, QLabel, QStyle, QToolBar, QVBoxLayout, QWidget, QHBoxLayout
)
from PySide6.QtCore import Qt, QDir, QSize, QFileInfo, QProcess
from PySide6.QtGui import QAction, QKeySequence, QTextCursor, QFont
from widgets.api_tester_widget import APITesterWidget
from widgets.code_editor import CodeEditor
from widgets.log_widget import LogWidget
from widgets.modern_toolbar import ModernToolbar
from widgets.find_replace_widget import FindReplaceWidget
# from widgets.minimap import Minimap
from widgets.breadcrumb_widget import BreadcrumbWidget
from theme.django_theme import DjangoTheme

                           
class DjangoStudioWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚀 Django Studio")
        self.resize(1400, 850)
        
        # Apply Django theme
        self.setStyleSheet(DjangoTheme.get_stylesheet())
        
        self.modern_toolbar = ModernToolbar()
        self.modern_toolbar.setStyleSheet(DjangoTheme.get_toolbar_stylesheet())
        self.addToolBar(self.modern_toolbar)
        
        # Connect toolbar signals
        self.modern_toolbar.run_server_clicked.connect(self.run_dev_server)
        self.modern_toolbar.stop_server_clicked.connect(self.stop_dev_server)
        self.modern_toolbar.make_migrations_clicked.connect(self.make_migrations)
        self.modern_toolbar.migrate_clicked.connect(self.run_migrate)
        
        self.open_files = {} 
        self.current_project_path = ""
        self.server_process = None

        self.setup_ui()
        
        menu = self.menuBar()
        menu.setStyleSheet(f"""
            QMenuBar {{
                background-color: {DjangoTheme.SECONDARY_BG};
                color: {DjangoTheme.TEXT_PRIMARY};
                border-bottom: 3px solid {DjangoTheme.DJANGO_GREEN};
            }}
            QMenuBar::item:selected {{
                background-color: {DjangoTheme.DJANGO_GREEN_ACCENT};
            }}
            QMenu {{
                background-color: {DjangoTheme.SECONDARY_BG};
                color: {DjangoTheme.TEXT_PRIMARY};
            }}
            QMenu::item:selected {{
                background-color: {DjangoTheme.DJANGO_GREEN};
            }}
        """)
        file_menu = menu.addMenu("File")
        
        open_action = QAction("Open Project Folder...", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_project_dialog)
        file_menu.addAction(open_action)
        

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
        self.project_tree.setStyleSheet(f"""
            QTreeView {{ 
                background-color: {DjangoTheme.SECONDARY_BG}; 
                color: {DjangoTheme.TEXT_PRIMARY}; 
                border: none; 
                font-size: 11px;
            }}
            QTreeView::item:hover {{ 
                background-color: {DjangoTheme.DJANGO_GREEN_ACCENT}; 
            }}
            QTreeView::item:selected {{ 
                background-color: {DjangoTheme.DJANGO_GREEN}; 
                color: white; 
            }}
        """)
        self.project_tree.doubleClicked.connect(self.open_file_from_tree)
        
        # Right: Editor + Logs/API
        right_splitter = QSplitter(Qt.Vertical)
        
        # 1. Editor Container with Find/Replace and Minimap
        editor_container = QWidget()
        editor_layout = QVBoxLayout(editor_container)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_layout.setSpacing(0)
        
        # Editor + Minimap horizontal layout
        editor_horizontal = QHBoxLayout()
        editor_horizontal.setContentsMargins(0, 0, 0, 0)
        editor_horizontal.setSpacing(0)
        
        self.editor_tabs = QTabWidget()
        self.editor_tabs.setTabsClosable(True)
        self.editor_tabs.setDocumentMode(True)
        self.editor_tabs.setStyleSheet(f"""
            QTabWidget::pane {{ border: none; }}
            QTabBar::tab {{ 
                background: {DjangoTheme.SECONDARY_BG}; 
                color: {DjangoTheme.TEXT_SECONDARY}; 
                padding: 10px 18px; 
                border: none;
                font-size: 11px;
            }}
            QTabBar::tab:selected {{ 
                background: {DjangoTheme.TERTIARY_BG}; 
                color: {DjangoTheme.TEXT_PRIMARY}; 
                border-bottom: 3px solid {DjangoTheme.ACCENT_PRIMARY}; 
            }}
            QTabBar::tab:hover {{
                background: {DjangoTheme.TERTIARY_BG};
            }}
        """)
        self.editor_tabs.tabCloseRequested.connect(self.close_tab)
        # self.editor_tabs.currentChanged.connect(self.on_editor_tab_changed)
        
        # Create minimap placeholder (will be populated when editor is added)
        self.current_minimap = None
        
        editor_horizontal.addWidget(self.editor_tabs, 1)
        
        # Find & Replace Widget (hidden by default)
        self.find_replace = FindReplaceWidget(parent=self)
        self.find_replace.hide()
        self.find_replace.close_requested.connect(self.hide_find_replace)
        
        # Breadcrumb Widget
        self.breadcrumb = BreadcrumbWidget(parent=self)
        self.breadcrumb.line_selected.connect(self.on_breadcrumb_selected)
        
        editor_layout.addWidget(self.find_replace)
        editor_layout.addWidget(self.breadcrumb)
        editor_layout.addLayout(editor_horizontal, 1)
        
        # 2. South Panel (Logs + API Tester)
        self.south_tabs = QTabWidget()
        self.south_tabs.setStyleSheet("""
            QTabWidget::pane { border: 0; }
            QTabBar::tab { background: #333333; color: #969696; padding: 5px 10px; }
            QTabBar::tab:selected { background: #1E1E1E; color: white; }
        """)

        # Tab 1: Terminal/Log
        self.log_widget = LogWidget()

        # Tab 2: API Tester
        self.api_tester = APITesterWidget()

        self.south_tabs.addTab(self.log_widget, "Terminal / Logs")
        self.south_tabs.addTab(self.api_tester, "API Tester")

        right_splitter.addWidget(editor_container)
        right_splitter.addWidget(self.south_tabs)
        right_splitter.setStretchFactor(0, 4)
        right_splitter.setStretchFactor(1, 1)

        main_splitter.addWidget(self.project_tree)
        main_splitter.addWidget(right_splitter)
        main_splitter.setStretchFactor(0, 1) 
        main_splitter.setStretchFactor(1, 5)
        
        self.setCentralWidget(main_splitter)

    # def setup_toolbar(self):
    #     toolbar = QToolBar("Django Controls")
    #     toolbar.setIconSize(QSize(20, 20))
    #     toolbar.setMovable(False)
    #     toolbar.setStyleSheet("QToolBar { background-color: #333333; border-bottom: 1px solid #444; spacing: 10px; padding: 5px; }")
    #     self.addToolBar(toolbar)

    #     def add_action(name, icon_type, method):
    #         icon = self.style().standardIcon(icon_type)
    #         action = QAction(icon, name, self)
    #         action.triggered.connect(method)
    #         toolbar.addAction(action)
    #         return action

    #     # Server Group
    #     toolbar.addWidget(QLabel(" SERVER:"))
    #     self.act_run = add_action("Run Server", QStyle.SP_MediaPlay, self.run_dev_server)
    #     self.act_stop = add_action("Stop Server", QStyle.SP_MediaStop, self.stop_dev_server)
    #     self.act_stop.setEnabled(False)
        
    #     toolbar.addSeparator()

    #     # Database Group
    #     toolbar.addWidget(QLabel(" DB: "))
    #     add_action("Make Migrations", QStyle.SP_FileIcon, self.make_migrations)
    #     add_action("Migrate", QStyle.SP_DialogApplyButton, self.run_migrate)

    #     toolbar.addSeparator()

    #     # Utils
    #     toolbar.addWidget(QLabel(" UTILS: "))
    #     add_action("New App", QStyle.SP_FileDialogNewFolder, self.open_new_app_dialog)

    # --- Actions ---
    def run_dev_server(self):
        if not self.current_project_path:
            QMessageBox.warning(self, "No Project", "Please open a project first.")
            self.modern_toolbar.update_status("Error: No Project", "#FF6B6B")
            return

        self.log_widget.append("\n--- Starting Django Server ---")
        self.south_tabs.setCurrentIndex(0) # Show Log Tab
        self.modern_toolbar.update_status("Server Starting...", "#FFD700")
        
        self.server_process = QProcess(self)
        self.server_process.setWorkingDirectory(self.current_project_path)
        self.server_process.readyReadStandardOutput.connect(self.handle_server_output)
        self.server_process.readyReadStandardError.connect(self.handle_server_error)
        self.server_process.finished.connect(self.on_server_finished)
        
        self.server_process.start("python", ["manage.py", "runserver"])
        
        # Update API Tester URL
        self.api_tester.set_server_context("http://127.0.0.1:8000/")
        self.modern_toolbar.set_server_running(True)

    def stop_dev_server(self):
        if self.server_process and self.server_process.state() == QProcess.Running:
            self.server_process.terminate()
            self.log_widget.append("--- Server Stopped ---")
            self.api_tester.set_server_context("Server Offline")
            self.modern_toolbar.set_server_running(False)
    
    def on_server_finished(self):
        """Handle server process finished"""
        self.modern_toolbar.set_server_running(False)

    def handle_server_output(self):
        data = self.server_process.readAllStandardOutput().data().decode()
        self.log_widget.insertPlainText(data)
        self.log_widget.ensureCursorVisible()
        
        # Update toolbar status if server is ready
        if "Starting development server" in data or "Quit the server with CONTROL-C" in data:
            self.modern_toolbar.set_server_running(True)
    
    def open_project_dialog(self):
        pass
    
    def handle_server_error(self):
        data = self.server_process.readAllStandardError().data().decode()
        self.log_widget.insertPlainText(data)
        self.log_widget.ensureCursorVisible()

    def make_migrations(self):
        self.log_widget.append("Running: makemigrations...")
        self.modern_toolbar.update_status("Making Migrations", "#FFD700")
        # Implementation to be added
    
    def run_migrate(self):
        self.log_widget.append("Running: migrate...")
        self.modern_toolbar.update_status("Running Migrations", "#FFD700")
        # Implementation to be added

    def open_new_app_dialog(self):
        QMessageBox.information(self, "New App", "Open Wizard to add apps.")
    
    # def on_editor_tab_changed(self, index):
    #     """Handle editor tab change to update minimap"""
    #     # Remove old minimap from horizontal layout
    #     layout = self.editor_tabs.parent().layout()
    #     for i in range(layout.count() - 1, -1, -1):
    #         item = layout.itemAt(i)
    #         if item:
    #             widget = item.widget()
    #             if isinstance(widget, Minimap):
    #                 widget.deleteLater()
    #                 layout.removeWidget(widget)
        
    #     # Add minimap for current editor
    #     current_editor = self.editor_tabs.currentWidget()
    #     if current_editor and isinstance(current_editor, CodeEditor):
    #         minimap = Minimap(current_editor)
    #         # Add minimap to the right of the editor tabs in horizontal layout
    #         self.editor_tabs.parent().layout().addWidget(minimap)
    #         self.current_minimap = minimap
            
    #         # Update breadcrumb
    #         self.breadcrumb.set_editor(current_editor)
    
    def on_breadcrumb_selected(self, line_num: int):
        """Handle breadcrumb item selection"""
        current_editor = self.editor_tabs.currentWidget()
        if current_editor and isinstance(current_editor, CodeEditor):
            # Move cursor to selected line
            block = current_editor.document().findBlockByLineNumber(line_num)
            cursor = QTextCursor(block)
            current_editor.setTextCursor(cursor)
            current_editor.ensureCursorVisible()

    # --- File System ---
    def set_project_path(self, path):
        self.current_project_path = path
        self.file_model.setRootPath(path)
        index = self.file_model.index(path)
        self.project_tree.setRootIndex(index)

    def close_tab(self, index):
        """Close a tab with unsaved file warning"""
        widget = self.editor_tabs.widget(index)
        
        # Check if file has unsaved changes
        if isinstance(widget, CodeEditor) and widget.is_dirty:
            file_path = widget.get_file_path()
            file_name = QFileInfo(file_path).fileName() if file_path else "Untitled"
            
            reply = QMessageBox.question(
                self, 
                "Unsaved Changes",
                f"'{file_name}' has unsaved changes. Do you want to save?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                QMessageBox.Save
            )
            
            if reply == QMessageBox.Cancel:
                return
            elif reply == QMessageBox.Save:
                self.save_file(file_path)
        
        # Remove from tracking
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
                new_editor.set_file_path(file_path)
                
                # Connect Find & Replace signals
                new_editor.find_requested.connect(self.show_find_replace)
                new_editor.dirty_changed.connect(lambda dirty: self.update_tab_title(file_path, dirty))
                new_editor.save_requested.connect(lambda: self.save_file(file_path))
                
                # Connect breadcrumb
                self.breadcrumb.set_editor(new_editor)
                
                # Update git gutter
                new_editor.update_git_gutter()
                
                self.find_replace.set_editor(new_editor)
                
                file_name = QFileInfo(file_path).fileName()
                new_index = self.editor_tabs.addTab(new_editor, file_name)
                self.editor_tabs.setCurrentIndex(new_index)
                self.open_files[file_path] = new_index
                
                # Mark as clean initially
                new_editor.set_dirty(False)
        except Exception as e:
            self.log_widget.append(f"Error opening file: {e}")
    
    def update_tab_title(self, file_path: str, is_dirty: bool):
        """Update tab title to show dirty indicator"""
        if file_path not in self.open_files:
            return
        
        tab_index = self.open_files[file_path]
        file_name = QFileInfo(file_path).fileName()
        
        # Add bullet point (•) to indicate unsaved changes
        display_name = f"• {file_name}" if is_dirty else file_name
        self.editor_tabs.setTabText(tab_index, display_name)
    
    def save_file(self, file_path: str):
        """Save the file to disk with auto-formatting"""
        if file_path not in self.open_files:
            return
        
        tab_index = self.open_files[file_path]
        editor = self.editor_tabs.widget(tab_index)
        
        if not editor or not isinstance(editor, CodeEditor):
            return
        
        try:
            # Auto-format code before saving
            editor.format_code_on_save()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(editor.toPlainText())
            
            # Mark as clean
            editor.set_dirty(False)
            self.log_widget.append(f"✓ File saved & formatted: {QFileInfo(file_path).fileName()}")
        except Exception as e:
            QMessageBox.warning(self, "Save Error", f"Could not save file:\n{e}")
            self.log_widget.append(f"✗ Error saving file: {e}")
    
    def show_find_replace(self):
        """Show the Find & Replace widget"""
        # Update editor reference to current editor
        current_editor = self.editor_tabs.currentWidget()
        if current_editor and isinstance(current_editor, CodeEditor):
            self.find_replace.set_editor(current_editor)
        
        self.find_replace.show()
        self.find_replace.focus_find_input()
    
    def hide_find_replace(self):
        """Hide the Find & Replace widget"""
        self.find_replace.hide()
        current_editor = self.editor_tabs.currentWidget()
        if current_editor:
            current_editor.setFocus()
