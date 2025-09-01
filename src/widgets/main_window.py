import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QTabWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Django Studio")
        self.setGeometry(100, 100, 1400, 900)
        self.initUI()
    
    def initUI(self):
        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        self.tab_widget.addTab(Editor(), "Editor")
        self.tab_widget.addTab(ModelDesiner(), "ModelDesiner")
        self.tab_widget.addTab(APITester(), "APITester")
        self.tab_widget.addTab(URLRouter(), "URLRouter")
        self.tab_widget.addTab(ProjectWizard(), "ProjectWizard")