from PySide6.QtWidgets import (QMainWindow, QMessageBox, QWidget, 
                                                       QVBoxLayout, QHBoxLayout, QPushButton, QFrame)
from PySide6.QtGui import QCloseEvent, QAction, QKeySequence
from PySide6.QtCore import Qt

from src.widgets.canvas import EditorCanvas
from src.widgets.properties import PropertiesPanel

class VectorEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Vector Editor")
        self.resize(1000, 700)

        # Trigger floating in window manager
        self.setWindowFlag(Qt.WindowType.Dialog, True)

        self._init_ui()
        
        print("Window initialized")

    def _init_ui(self):
        self._setup_layout()

        # Status bar
        self.statusBar().showMessage("Ready")

        # Menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")
        edit_menu = menubar.addMenu("&Edit")

        # Actions
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)

        group_action = QAction("Group", self)
        group_action.setShortcut("Ctrl+G")
        group_action.setStatusTip("Group selected shapes")
        group_action.triggered.connect(self.canvas.group_selection)

        ungroup_action = QAction("Ungroup", self)
        ungroup_action.setShortcut("Ctrl+U")
        ungroup_action.setStatusTip("Ungroup selected group")
        ungroup_action.triggered.connect(self.canvas.ungroup_selection)

        stack = self.canvas.undo_stack

        undo_action = stack.createUndoAction(self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)

        redo_action = stack.createRedoAction(self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)

        # Add actions to menu
        file_menu.addAction(exit_action)
        edit_menu.addAction(group_action)
        edit_menu.addAction(ungroup_action)
        edit_menu.addSeparator()
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)

        # Toolbar
        toolbar = self.addToolBar("File")
        toolbar.addAction(exit_action)
        toolbar.addSeparator()
        toolbar.addAction(group_action)
        toolbar.addAction(ungroup_action)
        toolbar.addSeparator()
        toolbar.addAction(undo_action)
        toolbar.addAction(redo_action)

    def _setup_layout(self):
        # 1. Create Main Container
        container = QWidget()
        self.setCentralWidget(container)

        # 2. Main Layout (Horizontal: Left Panel | Right Canvas)
        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # --- Left Panel (Tools) ---
        tools_panel = QFrame()
        tools_panel.setFixedWidth(120)
        tools_panel.setStyleSheet("background-color: #f0f0f0;")

        tools_layout = QVBoxLayout(tools_panel)

        self.btn_select = QPushButton("Select")
        self.btn_line = QPushButton("Line")
        self.btn_rect = QPushButton("Rect")
        self.btn_ellipse = QPushButton("Ellipse")

        self.btn_select.setCheckable(True)
        self.btn_line.setCheckable(True)
        self.btn_rect.setCheckable(True)
        self.btn_ellipse.setCheckable(True)

        self.btn_line.setChecked(True) # Default selected tool
        self.current_tool = "line"

        self.btn_select.clicked.connect(lambda: self.on_change_tool("selection"))
        self.btn_line.clicked.connect(lambda: self.on_change_tool("line"))
        self.btn_rect.clicked.connect(lambda: self.on_change_tool("rect"))
        self.btn_ellipse.clicked.connect(lambda: self.on_change_tool("ellipse"))

        tools_layout.addWidget(self.btn_select)
        tools_layout.addWidget(self.btn_line)
        tools_layout.addWidget(self.btn_rect)
        tools_layout.addWidget(self.btn_ellipse)
        tools_layout.addStretch() # Pushes buttons to the top

        # --- Right Part (Canvas) ---
        self.canvas = EditorCanvas()
        self.canvas.set_tool(self.current_tool)

        self_props_panel = PropertiesPanel(self.canvas.scene)
        
        # 3. Assemble
        main_layout.addWidget(tools_panel)
        main_layout.addWidget(self.canvas)
        main_layout.addWidget(self_props_panel)

    def on_change_tool(self, tool_name: str):
        self.current_tool = tool_name
        print("Tool selected:", tool_name)

        self.btn_select.setChecked(tool_name == "selection")
        self.btn_line.setChecked(tool_name == "line")
        self.btn_rect.setChecked(tool_name == "rect")
        self.btn_ellipse.setChecked(tool_name == "ellipse")

        self.canvas.set_tool(tool_name)

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