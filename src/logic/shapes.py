from PySide6.QtWidgets import QGraphicsPathItem, QGraphicsItemGroup
from PySide6.QtGui import QPen, QColor, QPainterPath

class Shape:
    @property
    def type_name(self) -> str:
        raise NotImplementedError

    def to_dict(self) -> dict:
        raise NotImplementedError

    def set_active_color(self, color: str):
        pass

    def set_geometry(self, start, end):
        pass

    def set_stroke_width(self, width: int):
        pass

class VectorShape(QGraphicsPathItem, Shape):
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
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsPathItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        
    def set_active_color(self, color: str):
        self.color = color
        self._setup_pen()

    def set_stroke_width(self, width: int):
        self.stroke_width = width
        self._setup_pen()

class Group(QGraphicsItemGroup, Shape):
    def __init__(self):
        super().__init__()
        self.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsMovable, True)
        self.setHandlesChildEvents(True)

    @property
    def type_name(self) -> str:
        return "group"

    def to_dict(self) -> dict:
        return {
            "type": self.type_name,
            "pos": [self.pos().x(), self.pos().y()],
            "children": [item.to_dict() for item in self.childItems() if isinstance(item, Shape)]
        }

    def set_geometry(self):
        pass  # Group geometry is managed by its children

    def set_active_color(self, color: str):
        for item in self.childItems():
            if isinstance(item, Shape):
                item.set_active_color(color)

    def set_stroke_width(self, width):
        for item in self.childItems():
            if isinstance(item, Shape):
                item.set_stroke_width(width)

class Rectangle(VectorShape):
    def __init__(self, x, y, w, h, color="black", stroke_width=2):
        super().__init__(color, stroke_width)
        self.w = w
        self.h = h
        self.setPos(x, y)
        self._create_geometry()

    def _create_geometry(self):
        path = QPainterPath()
        path.addRect(0, 0, self.w, self.h)
        self.setPath(path)

    def set_geometry(self, start_point, end_point):
        x = min(start_point.x(), end_point.x())
        y = min(start_point.y(), end_point.y())
        self.w = abs(end_point.x() - start_point.x())
        self.h = abs(end_point.y() - start_point.y())

        self.setPos(x, y)
        self._create_geometry()

    @property
    def type_name(self) -> str:
        return "rect"

    def to_dict(self) -> dict:
        return {
            "type": self.type_name,
            "pos": [self.pos().x(), self.pos().y()],
            "props": {
                "x": self.pos().x(), "y": self.pos().y(), 
                "w": self.w, "h": self.h,
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()
            }
        }

class Ellipse(VectorShape):
    def __init__(self, x, y, w, h, color="black", stroke_width=2):
        super().__init__(color, stroke_width)
        self.w = w
        self.h = h
        self.setPos(x, y)
        self._create_geometry()

    def _create_geometry(self):
        path = QPainterPath()
        path.addEllipse(0, 0, self.w, self.h)
        self.setPath(path)

    def set_geometry(self, start_point, end_point):
        x = min(start_point.x(), end_point.x())
        y = min(start_point.y(), end_point.y())
        self.w = abs(end_point.x() - start_point.x())
        self.h = abs(end_point.y() - start_point.y())
        self.setPos(x, y)
        self._create_geometry()

    @property
    def type_name(self) -> str:
        return "ellipse"

    def to_dict(self) -> dict:
        return {
            "type": self.type_name,
            "pos": [self.pos().x(), self.pos().y()],
            "props": {
                "x": self.pos().x(), "y": self.pos().y(), 
                "w": self.w, "h": self.h,
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()
            }
        }

class Line(VectorShape):
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

    def set_geometry(self, start_point, end_point):
        self.x1 = start_point.x()
        self.y1 = start_point.y()
        self.x2 = end_point.x()
        self.y2 = end_point.y()
        self._create_geometry()

    @property
    def type_name(self) -> str:
        return "line"

    def to_dict(self) -> dict:
        return {
            "type": self.type_name,
            "pos": [self.pos().x(), self.pos().y()],
            "props": {
                "x1": self.x1, "y1": self.y1,
                "x2": self.x2, "y2": self.y2,
                "color": self.pen().color().name(),
                "stroke_width": self.pen().width()
            }
        }