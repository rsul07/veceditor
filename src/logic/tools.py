from abc import ABC, abstractmethod
from PySide6.QtWidgets import QGraphicsView
from PySide6.QtCore import Qt, QPointF

from src.logic.factory import ShapeFactory
from src.logic.commands import AddShapeCommand, MoveCommand

class Tool(ABC):
    def __init__(self, view: QGraphicsView, undo_stack):
        self.view = view
        self.scene = view.scene
        self.undo_stack = undo_stack

    @abstractmethod
    def mouse_press(self, event): pass

    @abstractmethod
    def mouse_move(self, event): pass

    @abstractmethod
    def mouse_release(self, event): pass

class SelectionTool(Tool):
    def __init__(self, view: QGraphicsView, undo_stack):
        super().__init__(view, undo_stack)
        self.item_positions = {}

    def mouse_press(self, event):
        # Delegate to standard Qt logic (selection/moving)
        QGraphicsView.mousePressEvent(self.view, event)

        self.item_positions.clear()
        for item in self.scene.selectedItems():
            self.item_positions[item] = item.pos()

        # Cursor feedback
        item = self.view.itemAt(event.pos())
        if item:
            self.view.setCursor(Qt.CursorShape.ClosedHandCursor)

    def mouse_move(self, event):
        QGraphicsView.mouseMoveEvent(self.view, event)

        # Hover feedback logic
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            item = self.view.itemAt(event.pos())
            if item:
                self.view.setCursor(Qt.CursorShape.OpenHandCursor)
            else:
                self.view.setCursor(Qt.CursorShape.ArrowCursor)

    def mouse_release(self, event):
        QGraphicsView.mouseReleaseEvent(self.view, event)
        self.view.setCursor(Qt.CursorShape.ArrowCursor)

        moved_items = []
        for item, old_pos in self.item_positions.items():
            new_pos = item.pos()
            if old_pos != new_pos:
                moved_items.append((item, old_pos, new_pos))

        if moved_items:
            self.undo_stack.beginMacro("Move Items")
            for item, old_pos, new_pos in moved_items:
                command = MoveCommand(item, old_pos, new_pos)
                self.undo_stack.push(command)
            self.undo_stack.endMacro()

        self.item_positions.clear()

class CreationTool(Tool):
    def __init__(self, view, shape_type: str, undo_stack, color: str = "black"):
        super().__init__(view, undo_stack)
        self.shape_type = shape_type
        self.color = color
        self.start_pos = None
        self.temp_shape = None

    def mouse_press(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_pos = self.view.mapToScene(event.pos())
            try:
                # Create 0-size shape immediately
                self.temp_shape = ShapeFactory.create_shape(
                    self.shape_type, self.start_pos, self.start_pos, self.color
                )
                self.scene.addItem(self.temp_shape)
            except ValueError:
                pass

    def mouse_move(self, event):
        if self.temp_shape and self.start_pos:
            current_pos = self.view.mapToScene(event.pos())
            # Update geometry dynamically
            self.temp_shape.set_geometry(self.start_pos, current_pos)

    def mouse_release(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.start_pos:
            if self.temp_shape:
                self.scene.removeItem(self.temp_shape)
                self.temp_shape = None

            end_pos = self.view.mapToScene(event.pos())
            try:
                final_shape = ShapeFactory.create_shape(
                    self.shape_type, self.start_pos, end_pos, self.color
                )
                command = AddShapeCommand(self.scene, final_shape)
                self.undo_stack.push(command)
                print(f"Action {command.text()}")
            except ValueError:
                pass

            self.start_pos = None