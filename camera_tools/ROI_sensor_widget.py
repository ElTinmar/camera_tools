from qtpy.QtWidgets import QGraphicsRectItem, QGraphicsItem, QGraphicsView, QGraphicsScene, QFrame
from qtpy.QtGui import QColor, QPen, QBrush
from qtpy.QtCore import Qt, pyqtSignal

class InteractiveROIRect(QGraphicsRectItem):
    def __init__(self, parent_widget):
        super().__init__(0, 0, 1, 1)
        self.parent_widget = parent_widget
        
        self.setPen(QPen(QColor(255, 0, 0), 2))
        self.setBrush(QBrush(QColor(255, 0, 0, 40)))
        
        self.setFlags(
            QGraphicsItem.ItemIsMovable | 
            QGraphicsItem.ItemSendsGeometryChanges
        )

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            self.parent_widget.handle_rect_move(value)
        return super().itemChange(change, value)
    
class ROIGraphicalSelector(QGraphicsView):
    roi_moved = pyqtSignal(int, int)

    def __init__(self, parent=None, size=200):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        self.setFixedSize(size, size)
        self.setFrameStyle(QFrame.NoFrame)
        self.setAlignment(Qt.AlignCenter)
        self.setBackgroundBrush(QBrush(QColor(40, 40, 40))) 

        # The Sensor (Gray box)
        self.sensor_item = QGraphicsRectItem()
        self.sensor_item.setBrush(QBrush(QColor(180, 180, 180)))
        self.sensor_item.setPen(QPen(Qt.black, 1))
        self.scene.addItem(self.sensor_item)

        # The ROI (Red box)
        self.roi_item = InteractiveROIRect(self)
        self.scene.addItem(self.roi_item)

        self.sensor_w = 2048
        self.sensor_h = 1536
        self.scale_factor = 1.0
        self._is_updating = False
        self.padding = 10

    def update_roi_map(self, sensor_w, sensor_h, roi_w, roi_h, off_x, off_y):
        """Update the widget to reflect current hardware state."""
        self._is_updating = True
        self.sensor_w, self.sensor_h = sensor_w, sensor_h

        view_w, view_h = self.width() - self.padding, self.height() - self.padding
        self.scale_factor = min(view_w / sensor_w, view_h / sensor_h)

        self.sensor_item.setRect(0, 0, sensor_w * self.scale_factor, sensor_h * self.scale_factor)
        self.roi_item.setRect(0, 0, roi_w * self.scale_factor, roi_h * self.scale_factor)
        self.roi_item.setPos(off_x * self.scale_factor, off_y * self.scale_factor)
        
        self._is_updating = False

    def handle_rect_move(self, pos):
        """Convert graphical position back to hardware pixels."""
        if self._is_updating:
            return

        x = max(0, min(pos.x(), (self.sensor_w - self.roi_item.rect().width()/self.scale_factor) * self.scale_factor))
        y = max(0, min(pos.y(), (self.sensor_h - self.roi_item.rect().height()/self.scale_factor) * self.scale_factor))
        hardware_x = int(x / self.scale_factor)
        hardware_y = int(y / self.scale_factor)
        
        self.roi_moved.emit(hardware_x, hardware_y)

if __name__ == "__main__":
    
    import sys
    from qtpy.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel

    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("ROI Selector Test")
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)

    selector = ROIGraphicalSelector(size=300)
    layout.addWidget(selector)
    label = QLabel("Drag the red box to change OffsetX and OffsetY")
    label.setAlignment(Qt.AlignCenter)
    layout.addWidget(label)

    def on_roi_moved(x, y):
        label.setText(f"Hardware Coordinates -> OffsetX: {x}, OffsetY: {y}")
        print(f"Signal Received: X={x}, Y={y}")
    selector.roi_moved.connect(on_roi_moved)

    selector.update_roi_map(
        sensor_w=2048, 
        sensor_h=1536, 
        roi_w=640, 
        roi_h=480, 
        off_x=100, 
        off_y=100
    )

    window.show()
    sys.exit(app.exec_())