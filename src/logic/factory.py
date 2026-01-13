from src.logic.shapes import Rectangle, Line, Ellipse

class ShapeFactory:
    @staticmethod
    def create_shape(shape_type: str, start_point, end_point, color: str):
        """
        Creates a shape based on start/end mouse points.
        Handles normalization of coordinates (negative width/height).
        """
        x1, y1 = start_point.x(), start_point.y()
        x2, y2 = end_point.x(), end_point.y()

        # Lines don't need normalization
        if shape_type == 'line':
            return Line(x1, y1, x2, y2, color)

        # Normalize for Rect/Ellipse
        x = min(x1, x2)
        y = min(y1, y2)
        w = abs(x2 - x1)
        h = abs(y2 - y1)

        if shape_type == 'rect':
            return Rectangle(x, y, w, h, color)
        elif shape_type == 'ellipse':
            return Ellipse(x, y, w, h, color)
        else:
            raise ValueError(f"Unknown shape type: {shape_type}")