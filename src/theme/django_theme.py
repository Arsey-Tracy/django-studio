"""Django Studio Theme Configuration"""


class DjangoTheme:
    """Django-inspired color scheme and styling"""
    
    # Django Official Colors
    DJANGO_GREEN = "#092E20"        # Official Django green (dark)
    DJANGO_GREEN_LIGHT = "#44B78B"  # Light django green
    DJANGO_GREEN_ACCENT = "#0C4B33" # Medium green
    
    # UI Colors
    PRIMARY_BG = "#0F1419"          # Dark background
    SECONDARY_BG = "#1A1F26"        # Slightly lighter
    TERTIARY_BG = "#252B32"         # Editor background
    BORDER_COLOR = "#092E20"        # Django green border
    
    # Text Colors
    TEXT_PRIMARY = "#E8EEF5"        # Light text
    TEXT_SECONDARY = "#A8B5C4"      # Secondary text
    TEXT_MUTED = "#7A8895"          # Muted text
    
    # Accent Colors
    ACCENT_PRIMARY = "#44B78B"      # Django green light
    ACCENT_SECONDARY = "#FF9E64"    # Orange accent
    ACCENT_WARNING = "#FFD700"      # Warning yellow
    ACCENT_ERROR = "#FF6B6B"        # Error red
    
    # Status Colors
    STATUS_SUCCESS = "#44B78B"      # Green
    STATUS_ERROR = "#FF6B6B"        # Red
    STATUS_WARNING = "#FFD700"      # Yellow
    STATUS_INFO = "#0C90FF"         # Blue
    
    @staticmethod
    def get_stylesheet():
        """Get complete application stylesheet"""
        return f"""
            * {{
                color: {DjangoTheme.TEXT_PRIMARY};
            }}
            
            QMainWindow {{
                background-color: {DjangoTheme.PRIMARY_BG};
            }}
            
            QWidget {{
                background-color: {DjangoTheme.PRIMARY_BG};
                color: {DjangoTheme.TEXT_PRIMARY};
            }}
            
            QMenuBar {{
                background-color: {DjangoTheme.SECONDARY_BG};
                border-bottom: 2px solid {DjangoTheme.DJANGO_GREEN};
                color: {DjangoTheme.TEXT_PRIMARY};
            }}
            
            QMenuBar::item:selected {{
                background-color: {DjangoTheme.DJANGO_GREEN_ACCENT};
            }}
            
            QMenu {{
                background-color: {DjangoTheme.SECONDARY_BG};
                color: {DjangoTheme.TEXT_PRIMARY};
                border: 1px solid {DjangoTheme.BORDER_COLOR};
            }}
            
            QMenu::item:selected {{
                background-color: {DjangoTheme.DJANGO_GREEN_ACCENT};
                color: white;
            }}
            
            QTabBar::tab {{
                background-color: {DjangoTheme.SECONDARY_BG};
                color: {DjangoTheme.TEXT_SECONDARY};
                padding: 8px 15px;
                border: none;
            }}
            
            QTabBar::tab:selected {{
                background-color: {DjangoTheme.TERTIARY_BG};
                color: {DjangoTheme.TEXT_PRIMARY};
                border-bottom: 3px solid {DjangoTheme.ACCENT_PRIMARY};
            }}
            
            QTabBar::tab:hover {{
                background-color: {DjangoTheme.TERTIARY_BG};
            }}
            
            QTreeView {{
                background-color: {DjangoTheme.SECONDARY_BG};
                color: {DjangoTheme.TEXT_PRIMARY};
                border: none;
            }}
            
            QTreeView::item:hover {{
                background-color: {DjangoTheme.DJANGO_GREEN_ACCENT};
            }}
            
            QTreeView::item:selected {{
                background-color: {DjangoTheme.DJANGO_GREEN};
                color: white;
            }}
            
            QScrollBar:vertical {{
                background-color: {DjangoTheme.SECONDARY_BG};
                width: 12px;
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {DjangoTheme.DJANGO_GREEN};
                border-radius: 6px;
                min-height: 20px;
            }}
            
            QScrollBar::handle:vertical:hover {{
                background-color: {DjangoTheme.ACCENT_PRIMARY};
            }}
            
            QScrollBar:horizontal {{
                background-color: {DjangoTheme.SECONDARY_BG};
                height: 12px;
            }}
            
            QScrollBar::handle:horizontal {{
                background-color: {DjangoTheme.DJANGO_GREEN};
                border-radius: 6px;
                min-width: 20px;
            }}
            
            QScrollBar::handle:horizontal:hover {{
                background-color: {DjangoTheme.ACCENT_PRIMARY};
            }}
            
            QSplitter::handle {{
                background-color: {DjangoTheme.BORDER_COLOR};
            }}
        """
    
    @staticmethod
    def get_editor_stylesheet():
        """Get editor-specific stylesheet"""
        return f"""
            QTextEdit {{
                background-color: {DjangoTheme.TERTIARY_BG};
                color: {DjangoTheme.TEXT_PRIMARY};
                border: none;
            }}
        """
    
    @staticmethod
    def get_toolbar_stylesheet():
        """Get toolbar stylesheet"""
        return f"""
            QToolBar {{
                background-color: {DjangoTheme.SECONDARY_BG};
                border-bottom: 3px solid {DjangoTheme.DJANGO_GREEN};
                spacing: 12px;
                padding: 8px;
            }}
            
            QToolButton {{
                background-color: transparent;
                border: 2px solid transparent;
                border-radius: 6px;
                padding: 6px;
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
            
            QLabel {{
                color: {DjangoTheme.TEXT_PRIMARY};
                font-weight: bold;
            }}
        """
