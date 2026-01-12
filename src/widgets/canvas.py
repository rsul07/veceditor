from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter

class EditorCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.scene.setSceneRect(0, 0, 800, 600)
        self.setRenderHint(QPainter.Antialiasing) # Enable Antialiasing for smooth lines

        self.active_tool = None

    def set_tool(self, tool_name: str):
        self.active_tool = tool_name

    def mousePressEvent(self, event):
        scene_pos = self.mapToScene(event.pos())
        x, y = scene_pos.x(), scene_pos.y()

        print(f"Click at: {x:.1f}, {y:.1f} | Tool: {self.active_tool}")

        # Prototype drawing logic
        if event.button() == Qt.MouseButton.LeftButton:
            if self.active_tool == "line":
                # Draw a small diagonal line for testing
                self.scene.addLine(x, y, x + 50, y + 50)
            elif self.active_tool == "rect":
                self.scene.addRect(x, y, 50, 50)
            elif self.active_tool == "ellipse":
                self.scene.addEllipse(x, y, 50, 50)

        super().mousePressEvent(event)