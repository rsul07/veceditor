from abc import ABC, abstractmethod
from PySide6.QtWidgets import QGraphicsView
from PySide6.QtCore import Qt, QPointF
from src.logic.factory import ShapeFactory

class Tool(ABC):
    def __init__(self, view: QGraphicsView):
        self.view = view
        self.scene = view.scene()

    @abstractmethod
    def mouse_press(self, event): pass

    @abstractmethod
    def mouse_move(self, event): pass

    @abstractmethod
    def mouse_release(self, event): pass

class SelectionTool(Tool):
    def mouse_press(self, event):
        # Delegate to standard Qt logic (selection/moving)
        QGraphicsView.mousePressEvent(self.view, event)

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

class CreationTool(Tool):
    def __init__(self, view, shape_type: str, color: str = "black"):
        super().__init__(view)
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
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_pos = None
            self.temp_shape = None