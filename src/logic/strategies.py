from abc import ABC, abstractmethod
from PySide6.QtGui import QImage, QPainter, QColor
from PySide6.QtCore import QRectF
from src.logic.io_manager import FileManager

class SaveStrategy(ABC):
    @abstractmethod
    def save(self, filename: str, scene):
        """
        Abstract interface for saving.
        :param filename: Path to save
        :param scene: QGraphicsScene source
        """
        pass

class JsonSaveStrategy(SaveStrategy):
    def save(self, filename: str, scene):
        data = {
            "version": "1.0",
            "scene": {
                "width": scene.width(),
                "height": scene.height()
            },
            "shapes": []
        }

        items = scene.items()[::-1]

        for item in items:
            # Only save our custom shapes (ignore helper items)
            if hasattr(item, "to_dict"):
                data["shapes"].append(item.to_dict())

        FileManager.save_json(filename, data)

class ImageSaveStrategy(SaveStrategy):
    def __init__(self, fmt="PNG", bg_color="transparent"):
        self.fmt = fmt
        self.bg_color = bg_color

    def save(self, filename: str, scene):
        rect = scene.sceneRect()

        image = QImage(int(rect.width()), int(rect.height()), QImage.Format.Format_ARGB32)

        if self.bg_color == "transparent":
            image.fill(QColor(0, 0, 0, 0))
        else:
            image.fill(QColor(self.bg_color))

        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        scene.render(painter, QRectF(image.rect()), rect)
        painter.end()

        image.save(filename, self.fmt)