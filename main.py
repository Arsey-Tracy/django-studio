import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("Hello PySide6")
    window.setGeometry(100, 100, 400, 300)

    label = QLabel("Welcome to PySide6!", parent=window)
    label.setGeometry(100, 130, 200, 40)

    window.show()
    sys.exit(app.exec())

