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

class Rectangle(Shape):
    def __init__(self, x, y, w, h, color="black", stroke_width=2):
        super().__init__(color, stroke_width)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self._create_geometry()

    def _create_geometry(self):
        path = QPainterPath()
        path.addRect(self.x, self.y, self.w, self.h)
        self.setPath(path)

    @property
    def type_name(self) -> str:
        return "rect"

    def to_dict(self) -> dict:
        return {
            "type": self.type_name,
            "props": {
                "x": self.x, "y": self.y, 
                "w": self.w, "h": self.h,
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()
            }
        }

class Ellipse(Shape):
    def __init__(self, x, y, w, h, color="black", stroke_width=2):
        super().__init__(color, stroke_width)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self._create_geometry()

    def _create_geometry(self):
        path = QPainterPath()
        path.addEllipse(self.x, self.y, self.w, self.h)
        self.setPath(path)

    @property
    def type_name(self) -> str:
        return "ellipse"

    def to_dict(self) -> dict:
        return {
            "type": self.type_name,
            "props": {
                "x": self.x, "y": self.y, 
                "w": self.w, "h": self.h,
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()
            }
        }

class Line(Shape):
    def __init__(self, x1, y1, x2, y2, color="black", stroke_width=2):
        super().__init__(color, stroke_width)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self._create_geometry()

    def _create_geometry(self):
        path = QPainterPath()
        path.moveTo(self.x1, self.y1)
        path.lineTo(self.x2, self.y2)
        self.setPath(path)

    @property
    def type_name(self) -> str:
        return "line"

    def to_dict(self) -> dict:
        return {
            "type": self.type_name,
            "props": {
                "x1": self.x1, "y1": self.y1,
                "x2": self.x2, "y2": self.y2,
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()
            }
        }