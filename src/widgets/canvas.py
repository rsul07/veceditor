from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter

from src.logic.factory import ShapeFactory

class EditorCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.scene.setSceneRect(0, 0, 800, 600)
        self.setRenderHint(QPainter.Antialiasing) # Enable Antialiasing for smooth lines
        
        self.active_tool = "line"
        self.current_color = "black"
        self.start_point = None

    def set_tool(self, tool_name: str):
        self.active_tool = tool_name

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_point = self.mapToScene(event.pos())

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.start_point and event.button() == Qt.MouseButton.LeftButton:
            end_point = self.mapToScene(event.pos())

            try:
                new_shape = ShapeFactory.create_shape(
                    self.active_tool,
                    self.start_point,
                    end_point,
                    self.current_color
                )

                self.scene.addItem(new_shape)
                print(f"Created: {self.active_tool}")

            except ValueError:
                pass # Handle non-shape tools (like cursor)
            finally:
                self.start_point = None

        super().mouseReleaseEvent(event)