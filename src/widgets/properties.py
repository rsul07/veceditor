from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                               QSpinBox, QDoubleSpinBox, QPushButton, 
                               QColorDialog, QHBoxLayout)
from PySide6.QtCore import Qt

class PropertiesPanel(QWidget):
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self._init_ui()
        
        # PATTERN OBSERVER: Listen to selection changes
        self.scene.selectionChanged.connect(self.on_selection_changed)

    def _init_ui(self):
        self.setFixedWidth(200)
        self.setStyleSheet("background-color: #f0f0f0; border-left: 1px solid #ccc;")
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Title & Type Label
        title = QLabel("Properties")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        self.lbl_type = QLabel("None")
        self.lbl_type.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(self.lbl_type)
        
        # 1. Stroke Width
        layout.addWidget(QLabel("Stroke Width:"))
        self.spin_width = QSpinBox()
        self.spin_width.setRange(1, 50)
        self.spin_width.valueChanged.connect(self.on_width_changed)
        layout.addWidget(self.spin_width)
        
        # 2. Color
        layout.addWidget(QLabel("Color:"))
        self.btn_color = QPushButton()
        self.btn_color.setFixedHeight(30)
        self.btn_color.clicked.connect(self.on_color_clicked)
        layout.addWidget(self.btn_color)
        
        # 3. Geometry (X / Y)
        geo_layout = QHBoxLayout()
        self.spin_x = QDoubleSpinBox()
        self.spin_x.setRange(-10000, 10000)
        self.spin_x.setPrefix("X: ")
        self.spin_x.valueChanged.connect(self.on_geo_changed)
        
        self.spin_y = QDoubleSpinBox()
        self.spin_y.setRange(-10000, 10000)
        self.spin_y.setPrefix("Y: ")
        self.spin_y.valueChanged.connect(self.on_geo_changed)
        
        geo_layout.addWidget(self.spin_x)
        geo_layout.addWidget(self.spin_y)
        layout.addLayout(geo_layout)
        
        layout.addStretch()
        self.setEnabled(False)

    # --- MODEL -> VIEW (Read Data) ---
    def on_selection_changed(self):
        selected_items = self.scene.selectedItems()
        
        if not selected_items:
            self.setEnabled(False)
            self.lbl_type.setText("None")
            return

        self.setEnabled(True)
        item = selected_items[0]
        
        # Introspection
        type_text = "Unknown"
        if hasattr(item, "type_name"):
            type_text = item.type_name.capitalize()
        if len(selected_items) > 1:
            type_text += f" (+{len(selected_items)-1})"
        self.lbl_type.setText(type_text)

        # Update UI components without triggering signals back to model
        self.block_signals_ui(True)
        
        # Geometry
        self.spin_x.setValue(item.x())
        self.spin_y.setValue(item.y())
        
        # Style (Check if it has pen)
        if hasattr(item, "pen"):
            self.spin_width.setValue(item.pen().width())
            color = item.pen().color().name()
            self.btn_color.setStyleSheet(f"background-color: {color}; border: 1px solid gray;")
        
        self.block_signals_ui(False)

    def block_signals_ui(self, block: bool):
        self.spin_width.blockSignals(block)
        self.spin_x.blockSignals(block)
        self.spin_y.blockSignals(block)

    # --- VIEW -> MODEL (Write Data) ---
    def on_width_changed(self, value):
        for item in self.scene.selectedItems():
            if hasattr(item, "set_stroke_width"):
                item.set_stroke_width(value)
        self.scene.update()

    def on_color_clicked(self):
        color = QColorDialog.getColor()
        if color.isValid():
            hex_color = color.name()
            self.btn_color.setStyleSheet(f"background-color: {hex_color}; border: 1px solid gray;")
            
            for item in self.scene.selectedItems():
                if hasattr(item, "set_active_color"):
                    item.set_active_color(hex_color)
            self.scene.update()

    def on_geo_changed(self):
        new_x = self.spin_x.value()
        new_y = self.spin_y.value()
        
        for item in self.scene.selectedItems():
            item.setPos(new_x, new_y)