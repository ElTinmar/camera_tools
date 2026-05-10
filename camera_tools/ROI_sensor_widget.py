from qtpy.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                            QLabel, QGraphicsRectItem, QGraphicsItem, 
                            QGraphicsView, QGraphicsScene, QFrame, QPushButton)
from qtpy.QtGui import QColor, QPen, QBrush, QPainter, QPainterPath
from qtpy.QtCore import Qt, Signal as pyqtSignal, QRectF, QPointF

class ROIHandle(QGraphicsRectItem):
    """
    Stylized circular handles with hover expansion and high-contrast styling.
    """
    def __init__(self, index, handle_size, parent):
        # We use a slightly larger bounding box for the logic to prevent clipping
        super().__init__(-handle_size, -handle_size, handle_size*2, handle_size*2, parent)
        self.index = index
        self.handle_size = handle_size
        self.interaction_margin = 15 
        
        self.setAcceptHoverEvents(True)
        self.setZValue(2.0)
        self._hovered = False

    def shape(self):
        """Invisible hit-box for easier grabbing."""
        path = QPainterPath()
        s = (self.handle_size + self.interaction_margin) * 2
        path.addEllipse(QRectF(-s/2, -s/2, s, s))
        return path

    def paint(self, painter, option, widget):
        """Custom drawing for a 'pro' look."""
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Determine colors based on state
        color = QColor(255, 255, 0) if self._hovered else QColor(255, 255, 255)
        
        # Draw a subtle outer border/glow for visibility on any background
        painter.setPen(QPen(QColor(0, 0, 0, 150), 1.5))
        painter.setBrush(QBrush(color))
        
        # Draw the circle handle
        radius = self.handle_size / 2
        if self._hovered:
            radius += 2  # Slight pop-out effect on hover
            
        painter.drawEllipse(QPointF(0, 0), radius, radius)

    def hoverEnterEvent(self, event):
        self._hovered = True
        self.setCursor(Qt.SizeAllCursor)
        self.update() # Trigger repaint
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self._hovered = False
        self.unsetCursor()
        self.update()
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parentItem().start_resizing(self.index)
            event.accept()
        else:
            super().mousePressEvent(event)

class InteractiveROIRect(QGraphicsRectItem):

    def __init__(self, handle_size: int, parent_widget):
        super().__init__(0, 0, 1, 1)
        self.parent_widget = parent_widget
        self.handle_size = handle_size
        self.setPen(QPen(QColor(255, 0, 0), 2))
        self.setBrush(QBrush(QColor(255, 0, 0, 40)))
        
        self.setFlags(
            QGraphicsItem.ItemIsMovable | 
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemSendsGeometryChanges
        )
        
        # Enable hover events for the translate cursor icon
        self.setAcceptHoverEvents(True)
        
        self.handles = [ROIHandle(i, self.handle_size, self) for i in range(4)]
        self._resizing = False
        self._handle_index = -1
        self.update_handle_positions()

    def hoverEnterEvent(self, event):
        """Show move cursor when entering the ROI body."""
        self.setCursor(Qt.SizeAllCursor)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        """Clear cursor when leaving."""
        self.unsetCursor()
        super().hoverLeaveEvent(event)

    def update_handle_positions(self):
        """Update handles relative to the current rectangle."""
        r = self.rect()
        # 0:TL, 1:TR, 2:BL, 3:BR
        self.handles[0].setPos(r.left(), r.top())
        self.handles[1].setPos(r.right(), r.top())
        self.handles[2].setPos(r.left(), r.bottom())
        self.handles[3].setPos(r.right(), r.bottom())

    def start_resizing(self, index):
        """Logic triggered by a child handle click."""
        self._resizing = True
        self._handle_index = index
        self.grabMouse()
        self.setCursor(Qt.SizeAllCursor)

    def mouseMoveEvent(self, event):
        if self._resizing:
            self.resize_to_scene_pos(event.scenePos())
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self._resizing:
            self.ungrabMouse()
            self._resizing = False
            self._handle_index = -1
            # Check if we should keep the cursor based on whether we are still over the body
            if not self.contains(event.pos()):
                self.unsetCursor()
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def resize_to_scene_pos(self, scene_mouse_pos):
        self.prepareGeometryChange()
        sensor_rect = self.parent_widget.sensor_item.rect()
        
        # Clamp to sensor area
        cx = max(0, min(scene_mouse_pos.x(), sensor_rect.width()))
        cy = max(0, min(scene_mouse_pos.y(), sensor_rect.height()))

        r = self.rect()
        p = self.pos()
        g_left, g_top = p.x() + r.left(), p.y() + r.top()
        g_right, g_bottom = g_left + r.width(), g_top + r.height()
        
        min_dim = self.handle_size 

        # x1,y1 is new TopLeft | x2,y2 is new BottomRight (Global scene coords)
        if self._handle_index == 0: # TL
            x1, y1, x2, y2 = min(cx, g_right-min_dim), min(cy, g_bottom-min_dim), g_right, g_bottom
        elif self._handle_index == 1: # TR
            x1, y1, x2, y2 = g_left, min(cy, g_bottom-min_dim), max(cx, g_left+min_dim), g_bottom
        elif self._handle_index == 2: # BL
            x1, y1, x2, y2 = min(cx, g_right-min_dim), g_top, g_right, max(cy, g_top+min_dim)
        elif self._handle_index == 3: # BR
            x1, y1, x2, y2 = g_left, g_top, max(cx, g_left+min_dim), max(cy, g_top+min_dim)

        self.setPos(x1, y1)
        self.setRect(0, 0, x2 - x1, y2 - y1)
        self.update_handle_positions()
        self.parent_widget.handle_rect_change()

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            if self._resizing:
                return value 
            
            # Boundary clamping for translation
            new_pos = value
            sensor = self.parent_widget.sensor_item.rect()
            roi = self.rect()

            x = max(0, min(new_pos.x(), sensor.width() - roi.width()))
            y = max(0, min(new_pos.y(), sensor.height() - roi.height()))
            
            constrained = QPointF(x, y)
            self.parent_widget.handle_rect_change(forced_pos=constrained)
            return constrained
            
        return super().itemChange(change, value)
    
class ROIGraphicalSelector(QGraphicsView):
    roi_changed = pyqtSignal(int, int, int, int)
    HANDLE_SIZE = 10

    def __init__(self, parent=None, size=150):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        
        # UI Configuration
        self.setFixedSize(size, size)
        self.setFrameStyle(QFrame.NoFrame)
        self.setBackgroundBrush(QBrush(QColor(35, 35, 35))) 
        self.setRenderHint(QPainter.Antialiasing)
        self.setBackgroundBrush(QBrush(Qt.NoBrush))
        self.setStyleSheet("background: transparent;")
        self.setAlignment(Qt.AlignCenter)
    
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.sensor_item = QGraphicsRectItem()
        self.sensor_item.setBrush(QBrush(QColor(170, 170, 170)))
        self.sensor_item.setPen(QPen(Qt.black, 1))
        self.scene.addItem(self.sensor_item)

        self.roi_item = InteractiveROIRect(self.HANDLE_SIZE, self)
        self.scene.addItem(self.roi_item)

        self.scale_factor = 1.0
        self._is_updating = False

    def update_roi_map(self, sensor_w, sensor_h, roi_w, roi_h, off_x, off_y):

        self._is_updating = True
        
        view_padding = self.HANDLE_SIZE + 10
        
        # Calculate scale factor to fit the sensor into the widget size
        self.scale_factor = min(
            (self.width() - view_padding) / sensor_w, 
            (self.height() - view_padding) / sensor_h
        )

        # Scale the sensor background
        s_w_scaled = sensor_w * self.scale_factor
        s_h_scaled = sensor_h * self.scale_factor
        self.sensor_item.setRect(0, 0, s_w_scaled, s_h_scaled)

        # Scale and position the ROI
        self.roi_item.setRect(0, 0, roi_w * self.scale_factor, roi_h * self.scale_factor)
        self.roi_item.setPos(off_x * self.scale_factor, off_y * self.scale_factor)
        self.roi_item.update_handle_positions()
        
        self.setSceneRect(self.sensor_item.rect())
        self.centerOn(self.sensor_item.rect().center())
        
        self._is_updating = False

    def handle_rect_change(self, forced_pos=None):
        if self._is_updating: 
            return
            
        pos = forced_pos if forced_pos else self.roi_item.pos()
        rect = self.roi_item.rect()
        
        # Divide by scale_factor to return to 1:1 camera sensor pixels
        real_x = int(pos.x() / self.scale_factor)
        real_y = int(pos.y() / self.scale_factor)
        real_w = int(rect.width() / self.scale_factor)
        real_h = int(rect.height() / self.scale_factor)
        
        self.roi_changed.emit(real_x, real_y, real_w, real_h)

class CameraSensorROI(QWidget):
    """
    Container widget combining the Graphical ROI Selector and a 
    utility button to center the ROI on the sensor.
    """
    roi_changed = pyqtSignal(int, int, int, int)

    def __init__(self, parent=None, selector_size=150):
        super().__init__(parent)
        
        # State tracking for centering math
        self.last_sensor_w = 2000
        self.last_sensor_h = 2000
        self.last_roi_w = 1000
        self.last_roi_h = 1000

        self.init_ui(selector_size)

    def init_ui(self, selector_size):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addStretch()

        # 1. The Graphical Selector
        self.selector = ROIGraphicalSelector(size=selector_size)
        self.selector.roi_changed.connect(self.handle_selector_change)
        layout.addWidget(self.selector, alignment=Qt.AlignCenter)

        # 2. The Auto-Center Button
        self.center_button = QPushButton("Center ROI")
        self.center_button.setToolTip("Move the ROI to the center of the sensor")
        self.center_button.clicked.connect(self.center_roi)
        layout.addWidget(self.center_button)
        layout.addStretch()

    def handle_selector_change(self, x, y, w, h):
        """Pass the signal up and cache values for centering math."""
        self.last_roi_w, self.last_roi_h = w, h
        self.roi_changed.emit(x, y, w, h)

    def update_roi_map(self, sensor_w, sensor_h, roi_w, roi_h, off_x, off_y):
        """Standard passthrough to update the visual map."""
        self.last_sensor_w = sensor_w
        self.last_sensor_h = sensor_h
        self.last_roi_w = roi_w
        self.last_roi_h = roi_h
        
        self.selector.update_roi_map(sensor_w, sensor_h, roi_w, roi_h, off_x, off_y)

    def center_roi(self):
        """Calculates center offsets and emits the change."""
        # Calculate offsets to center the current ROI width/height on the sensor
        new_x = max(0, (self.last_sensor_w - self.last_roi_w) // 2)
        new_y = max(0, (self.last_sensor_h - self.last_roi_h) // 2)
        
        # We emit the signal so the CameraWidget/Backend knows to update
        self.roi_changed.emit(new_x, new_y, self.last_roi_w, self.last_roi_h)
        
        # Update visual representation immediately
        self.selector.update_roi_map(
            self.last_sensor_w, 
            self.last_sensor_h, 
            self.last_roi_w, 
            self.last_roi_h, 
            new_x, 
            new_y
        )

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setWindowTitle("Polished Camera ROI Control")
    cw = QWidget(); win.setCentralWidget(cw); layout = QVBoxLayout(cw)
    selector = CameraSensorROI(selector_size=600); layout.addWidget(selector)
    label = QLabel("OFFSET: 0, 0 | SIZE: 0x0"); label.setAlignment(Qt.AlignCenter); layout.addWidget(label)
    
    selector.roi_changed.connect(lambda x,y,w,h: label.setText(f"OFFSET: {x}, {y} | SIZE: {w}x{h}"))
    
    # Initial setup: 2MP sensor, 800x600 ROI
    selector.update_roi_map(2048, 2048, 800, 800, 100, 100)
    
    win.show()
    sys.exit(app.exec_())