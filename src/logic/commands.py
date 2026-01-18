from PySide6.QtGui import QUndoCommand

class AddShapeCommand(QUndoCommand):
    def __init__(self, scene, item):
        super().__init__()
        self.scene = scene
        self.item = item
        
        # Get a nice name for the history list
        name = "Shape"
        if hasattr(item, "type_name"):
            name = item.type_name
        self.setText(f"Add {name}")

    def redo(self):
        # Called on push() and Redo
        # Prevent double addition if already in scene
        if self.item.scene() != self.scene:
            self.scene.addItem(self.item)

    def undo(self):
        # Called on Undo
        self.scene.removeItem(self.item)