from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter

class EditorCanvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.scene.setSceneRect(0, 0, 800, 600)
        
        # Enable Antialiasing for smooth lines
        self.setRenderHint(QPainter.Antialiasing)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.scene.addText("Hello, Vector World!").setPos(350, 280)