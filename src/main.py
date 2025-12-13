import sys
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import (
    QApplication
)
from ui.main_window import DjangoStudioWindow
from widgets.project_wizard import ProjectWizard
from ui.welcome_window import WelcomeWindow
class DjangoStudioApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.show_welcome()
        sys.exit(self.app.exec())
    
    def show_welcome(self):
        self.welcome = WelcomeWindow()
        self.welcome.project_selected.connect(self.launch_editor)
        self.welcome.request_new_project.connect(self.show_wizard)
        self.welcome.show()
    
    def show_wizard(self):
        self.welcome.close()
        self.wizard = ProjectWizard()
        self.wizard.project_ready.connect(self.launch_editor_from_wizard)
        self.wizard.show()
    
    def launch_editor_from_wizard(self, path):
        # Update settings for recent list
        settings = QSettings("DjangoStudio", "RecentProjects")
        recents = settings.value("paths", []) or []
        if path not in recents:
            recents.insert(0, path)
            settings.setValue("paths", recents)
        
        self.launch_editor(path)
    
    def launch_editor(self, project_path):
        if hasattr(self, 'welcome'): self.welcome.close()
        if hasattr(self, 'wizard'): self.wizard.close()
        
        self.main_window = DjangoStudioWindow()
        self.main_window.set_project_path(project_path)
        self.main_window.log_widget.append(f"Project loaded: {project_path}")
        self.main_window.show()


if __name__ == "__main__":
    DjangoStudioApp()
      