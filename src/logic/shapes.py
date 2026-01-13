from abc import ABC, abstractmethod
from PySide6.QtWidgets import QGraphicsPathItem
from PySide6.QtGui import QPen, QColor, QPainterPath

class Shape(QGraphicsPathItem, ABC):
    def __init__(self, color: str = "black", stroke_width: int = 2):
        super().__init__() 
        
        self.color = color
        self.stroke_width = stroke_width
        
        self._setup_pen()
        self._setup_flags()

    def _setup_pen(self):
        pen = QPen(QColor(self.color))
        pen.setWidth(self.stroke_width)
        self.setPen(pen)

    def _setup_flags(self):
        # Enable selection and movement logic provided by Qt
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemSendsGeometryChanges)

    # --- Abstract Contract ---

    @property
    @abstractmethod
    def type_name(self) -> str:
        """String identifier for the shape type"""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Serialize shape data to dictionary"""
        pass
        
    # --- Common Methods ---
    
    def set_active_color(self, color: str):
        self.color = color
        self._setup_pen()