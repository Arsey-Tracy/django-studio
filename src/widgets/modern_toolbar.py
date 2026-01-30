from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QToolButton,
    QToolBar, QMessageBox, QStatusBar, QSizePolicy
)
from PySide6.QtCore import QSize, Qt, QTimer, Signal
from PySide6.QtGui import QIcon, QColor
from pathlib import Path
from theme.django_theme import DjangoTheme

class ModernToolbar(QToolBar):
    """Enhanced toolbar with SVG icons and Django-themed styling"""
    
    # Signals for main window to connect
    run_server_clicked = Signal()
    stop_server_clicked = Signal()
    make_migrations_clicked = Signal()
    migrate_clicked = Signal()
    
    def __init__(self):
        super().__init__()
        self.setIconSize(QSize(24, 24))
        self.setMovable(False)
        self.setFloatable(False)
        
        self.current_project_path = ""
        self.server_process = None
        self.server_running = False
        
        # Get assets directory
        self.assets_dir = Path(__file__).parent.parent / "assets" / "icons"
        
        # Django-themed styling
        self.setStyleSheet(f"""
            QToolBar {{
                background-color: {DjangoTheme.SECONDARY_BG};
                border-bottom: 3px solid {DjangoTheme.DJANGO_GREEN};
                spacing: 16px;
                padding: 8px 12px;
            }}
            QToolButton {{
                background-color: transparent;
                border: 2px solid transparent;
                border-radius: 6px;
                padding: 8px;
                margin: 2px;
                color: {DjangoTheme.TEXT_PRIMARY};
            }}
            QToolButton:hover {{
                background-color: {DjangoTheme.DJANGO_GREEN_ACCENT};
                border: 2px solid {DjangoTheme.ACCENT_PRIMARY};
            }}
            QToolButton:pressed {{
                background-color: {DjangoTheme.ACCENT_PRIMARY};
                color: white;
            }}
            QToolButton:checked {{
                background-color: {DjangoTheme.ACCENT_PRIMARY};
                border: 2px solid {DjangoTheme.STATUS_SUCCESS};
            }}
            QLabel {{
                color: {DjangoTheme.TEXT_PRIMARY};
                font-weight: bold;
                font-size: 11px;
                margin: 0px 8px 0px 12px;
            }}
            QFrame {{
                background-color: transparent;
            }}
        """)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Build the toolbar UI"""
        # Stretch at start
        stretch = QWidget()
        stretch.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.addWidget(stretch)
        
        # --- SERVER GROUP ---
        server_group = self.create_group("▶ SERVER", [
            ("play.svg", "Run Dev Server", self.run_dev_server, False),
            ("stop.svg", "Stop Server", self.stop_dev_server, False),
        ])
        self.addWidget(server_group)
        
        self.addSeparator()
        
        # --- DATABASE GROUP ---
        db_group = self.create_group("⚙ DATABASE", [
            ("database.svg", "Make Migrations", self.make_migrations, False),
            ("arrow-up.svg", "Migrate", self.run_migrate, False),
        ])
        self.addWidget(db_group)
        
        self.addSeparator()
        
        # --- TOOLS GROUP ---
        tools_group = self.create_group("🔧 TOOLS", [
            ("plus.svg", "New App", self.open_new_app_dialog, False),
            ("terminal.svg", "Terminal", self.open_terminal, False),
        ])
        self.addWidget(tools_group)
        
        # Stretch at end
        end_stretch = QWidget()
        end_stretch.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.addWidget(end_stretch)
        
        # --- STATUS LABEL ---
        self.status_label = QLabel("● Ready")
        self.status_label.setStyleSheet("color: #4EC9B0; font-weight: bold;")
        self.addWidget(self.status_label)
    
    def create_group(self, label_text: str, buttons: list):
        """Create a toolbar group with label and buttons"""
        group = QFrame()
        group.setStyleSheet("QFrame { background-color: #252526; border-radius: 4px; margin: 0px 4px; }")
        layout = QHBoxLayout(group)
        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(2)
        
        # Group label
        label = QLabel(label_text)
        label.setStyleSheet("color: #989898; font-size: 10px; font-weight: bold; margin: 4px 6px 4px 6px;")
        layout.addWidget(label)
        
        # Add separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setStyleSheet("color: #3E3E42; margin: 2px 4px;")
        separator.setMaximumWidth(1)
        layout.addWidget(separator)
        
        # Add buttons
        for icon_file, tooltip, callback, checkable in buttons:
            btn = self.create_icon_button(icon_file, tooltip, callback, checkable)
            layout.addWidget(btn)
        
        return group
    
    def create_icon_button(self, icon_file: str, tooltip: str, callback, checkable: bool = False):
        """Create a tool button with SVG icon"""
        btn = QToolButton()
        btn.setToolTip(tooltip)
        btn.clicked.connect(callback)
        btn.setFixedSize(36, 32)
        btn.setIconSize(QSize(20, 20))
        btn.setCheckable(checkable)
        
        # Load SVG icon with color
        icon_path = self.assets_dir / icon_file
        if icon_path.exists():
            # Read and colorize SVG
            with open(icon_path, 'r') as f:
                svg_content = f.read()
            
            # Replace stroke and fill with icon color
            svg_content = svg_content.replace('currentColor', '#D4D4D4')
            svg_content = svg_content.replace('stroke="currentColor"', 'stroke="#D4D4D4"')
            
            # Save temporary colored SVG and create icon
            icon = QIcon(str(icon_path))
            btn.setIcon(icon)
        
        return btn
    
    def update_status(self, status: str, color: str = "#4EC9B0"):
        """Update the status label"""
        self.status_label.setText(f"● {status}")
        self.status_label.setStyleSheet(f"color: {color}; font-weight: bold;")
    
    def set_server_running(self, running: bool):
        """Set server running state and update UI"""
        self.server_running = running
        if running:
            self.update_status("Server Running", "#00FF00")
        else:
            self.update_status("Ready", "#4EC9B0")

    def run_dev_server(self):
        """Run development server"""
        self.run_server_clicked.emit()
        self.set_server_running(True)
    
    def stop_dev_server(self):
        """Stop development server"""
        self.stop_server_clicked.emit()
        self.set_server_running(False)
    
    def make_migrations(self):
        """Make migrations"""
        self.make_migrations_clicked.emit()
        self.update_status("Making Migrations...", "#FFD700")
        QTimer.singleShot(2000, lambda: self.update_status("Ready"))
    
    def run_migrate(self):
        """Run migrations"""
        self.migrate_clicked.emit()
        self.update_status("Running Migrations...", "#FFD700")
        QTimer.singleShot(2000, lambda: self.update_status("Ready"))
    
    def open_new_app_dialog(self):
        """Open new app dialog"""
        QMessageBox.information(self, "New App", "New App Wizard (coming soon)")
    
    def open_terminal(self):
        """Open terminal"""
        QMessageBox.information(self, "Terminal", "Integrated Terminal (coming soon)")