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

class MoveCommand(QUndoCommand):
    def __init__(self, item, old_pos, new_pos):
        super().__init__()
        self.item = item
        self.old_pos = old_pos
        self.new_pos = new_pos
        
        self.setText(f"Move {getattr(item, 'type_name', 'Item')}")

    def redo(self):
        self.item.setPos(self.new_pos)

    def undo(self):
        self.item.setPos(self.old_pos)

class DeleteCommand(QUndoCommand):
    def __init__(self, scene, item):
        super().__init__()
        self.scene = scene
        self.item = item
        
        self.setText(f"Delete {getattr(item, 'type_name', 'Item')}")

    def redo(self):
        self.scene.removeItem(self.item)

    def undo(self):
        self.scene.addItem(self.item)