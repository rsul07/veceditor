from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtGui import QCloseEvent

class VectorEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Vector Editor")
        self.resize(800, 600)

        self._init_ui()
        
        print("Window initialized")

    def _init_ui(self):
        self.statusBar().showMessage("Ready")

    def closeEvent(self, event: QCloseEvent):
        reply = QMessageBox.question(
            self,
            "Confirm exit",
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            event.accept()
            print("Window closed")
        else:
            event.ignore()
            print("Exit canceled")