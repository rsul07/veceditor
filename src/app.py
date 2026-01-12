from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtGui import QCloseEvent, QAction
from PySide6.QtCore import Qt

class VectorEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Vector Editor")
        self.resize(800, 600)

        # Trigger floating in window manager
        self.setWindowFlag(Qt.WindowType.Dialog, True)

        self._init_ui()
        
        print("Window initialized")

    def _init_ui(self):
        # Status bar
        self.statusBar().showMessage("Ready")

        # Menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")

        # Actions
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)

        file_menu.addAction(exit_action)

        toolbar = self.addToolBar("File")
        toolbar.addAction(exit_action)

        self._setup_layout()

    def _setup_layout(self):
        # Setup layout
        pass

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