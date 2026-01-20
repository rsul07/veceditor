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

class ChangeColorCommand(QUndoCommand):
    def __init__(self, item, new_color):
        super().__init__()
        self.item = item
        self.new_color = new_color

        # Save old color for undo
        if hasattr(item, "pen"):
            self.old_color = item.pen().color().name()
        else:
            self.old_color = "#000000"

        self.setText(f"Change Color to {new_color}")

    def redo(self):
        if hasattr(self.item, "set_active_color"):
            self.item.set_active_color(self.new_color)

    def undo(self):
        if hasattr(self.item, "set_active_color"):
            self.item.set_active_color(self.old_color)

class ChangeWidthCommand(QUndoCommand):
    def __init__(self, item, new_width):
        super().__init__()
        self.item = item
        self.new_width = new_width

        # Save old width
        if hasattr(item, "pen"):
            self.old_width = item.pen().width()
        else:
            self.old_width = 1

        self.setText(f"Change Width to {new_width}")

    def redo(self):
        if hasattr(self.item, "set_stroke_width"):
            self.item.set_stroke_width(self.new_width)

    def undo(self):
        if hasattr(self.item, "set_stroke_width"):
            self.item.set_stroke_width(self.old_width)

class ChangePosCommand(QUndoCommand):
    def __init__(self, item, new_pos):
        super().__init__()
        self.item = item
        self.new_pos = new_pos

        # Save old position
        self.old_pos = item.pos()

        self.setText(f"Change Position to {new_pos}")

    def redo(self):
        self.item.setPos(self.new_pos)

    def undo(self):
        self.item.setPos(self.old_pos)