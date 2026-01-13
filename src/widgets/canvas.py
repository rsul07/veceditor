from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter

from src.logic.factory import ShapeFactory
from src.logic.tools import SelectionTool, CreationTool

class EditorCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.scene.setSceneRect(0, 0, 800, 600)
        self.setRenderHint(QPainter.Antialiasing) # Enable Antialiasing for smooth lines

        self.tools = {
            "selection": SelectionTool(self),
            "line": CreationTool(self, "line"),
            "rect": CreationTool(self, "rect"),
            "ellipse": CreationTool(self, "ellipse"),
        }

        self.active_tool = self.tools["line"] 
        self.current_color = "black"

    def set_tool(self, tool_name: str):
        if tool_name in self.tools:
            self.active_tool = self.tools[tool_name]

        # Cursor logic
        if tool_name == "selection":
            self.setCursor(Qt.CursorShape.ArrowCursor)
        else:
            self.setCursor(Qt.CursorShape.CrossCursor)

    def mousePressEvent(self, event):
        self.active_tool.mouse_press(event)

    def mouseMoveEvent(self, event):
        self.active_tool.mouse_move(event)

    def mouseReleaseEvent(self, event):
        self.active_tool.mouse_release(event)