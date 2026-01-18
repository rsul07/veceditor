from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QUndoStack

from src.logic.shapes import Group
from src.logic.tools import SelectionTool, CreationTool

class EditorCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.scene.setSceneRect(0, 0, 800, 600)
        self.setRenderHint(QPainter.Antialiasing) # Enable Antialiasing for smooth lines

        self.undo_stack = QUndoStack(self)
        self.undo_stack.setUndoLimit(50)

        self.tools = {
            "selection": SelectionTool(self, self.undo_stack),
            "line": CreationTool(self, "line", self.undo_stack),
            "rect": CreationTool(self, "rect", self.undo_stack),
            "ellipse": CreationTool(self, "ellipse", self.undo_stack),
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

    def group_selection(self):
        selected_items = self.scene.selectedItems()
        if len(selected_items) < 1:
            return  # Need at least two items to group

        group = Group()
        self.scene.addItem(group)

        for item in selected_items:
            item.setSelected(False)
            group.addToGroup(item)

        group.setSelected(True)
        print("Group created")

    def ungroup_selection(self):
        selected_items = self.scene.selectedItems()
        for item in selected_items:
            if isinstance(item, Group):
                self.scene.destroyItemGroup(item)
                print("Group destroyed")

    def mousePressEvent(self, event):
        self.active_tool.mouse_press(event)

    def mouseMoveEvent(self, event):
        self.active_tool.mouse_move(event)

    def mouseReleaseEvent(self, event):
        self.active_tool.mouse_release(event)