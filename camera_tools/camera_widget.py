# TODO record to file ?

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGroupBox
from qt_widgets import LabeledDoubleSpinBox, LabeledSliderSpinBox, NDarray_to_QPixmap
from camera_tools.camera import Camera
#from ipc_tools import QueueLike

# TODO adjust display FPS and add a queue to receive images from the camera
# TODO show camera FPS, display FPS, and camera statistics in status bar
# TODO subclass CameraWidget for camera with specifi controls

class CameraWidget(QWidget):

    def __init__(self, camera: Camera, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.camera = camera
        self.acquisition_started = False
        
        self.declare_components()
        self.layout_components()
        self.set_timers()

    # UI ---------------------------------------------------------
    
    def create_spinbox(self, attr: str):
        '''
        Creates spinbox with correct label, value, range and increment
        as specified by the camera object. Connects to relevant
        callback.
        WARNING This is compact but a bit terse and introduces dependencies
        in the code. 
        '''
        setattr(self, attr + '_spinbox', LabeledDoubleSpinBox(self))
        spinbox = getattr(self, attr + '_spinbox')
        callback = getattr(self, 'set_' + attr)
        spinbox.setText(attr)
        spinbox.valueChanged.connect(callback)
        value = getattr(self.camera, 'get_' + attr)()
        range = getattr(self.camera, 'get_' + attr + '_range')()
        increment = getattr(self.camera, 'get_' + attr + '_increment')()
        
        if (
            value is not None 
            and range is not None
            and increment is not None
        ):
            spinbox.setRange(range[0],range[1])
            spinbox.setSingleStep(increment)
            spinbox.setValue(value)
        else:
            spinbox.setDisabled(True)
            
    def declare_components(self):

        # Image --------------------------------------------------

        self.image_label = QLabel(self) 

        # Basic camera controls ----------------------------------
         
        self.start_button = QPushButton(self)
        self.start_button.setText('start')
        self.start_button.clicked.connect(self.start_acquisition)

        self.stop_button = QPushButton(self)
        self.stop_button.setText('stop')
        self.stop_button.clicked.connect(self.stop_acquisition)

        # controls 

        self.create_spinbox('framerate')
        self.create_spinbox('exposure')
        self.create_spinbox('gain')
        self.create_spinbox('offsetX')
        self.create_spinbox('offsetY')
        self.create_spinbox('height')
        self.create_spinbox('width')

        # Region of interest ------------------------------------

        self.ROI_groupbox = QGroupBox('ROI:')

    def layout_components(self):

        layout_start_stop = QHBoxLayout()
        layout_start_stop.addWidget(self.start_button)
        layout_start_stop.addWidget(self.stop_button)

        layout_frame = QVBoxLayout(self.ROI_groupbox)
        layout_frame.addWidget(self.offsetX_spinbox)
        layout_frame.addWidget(self.offsetY_spinbox)
        layout_frame.addWidget(self.height_spinbox)
        layout_frame.addWidget(self.width_spinbox)

        layout_controls = QVBoxLayout()
        layout_controls.addWidget(self.exposure_spinbox)
        layout_controls.addWidget(self.gain_spinbox)
        layout_controls.addWidget(self.framerate_spinbox)
        layout_controls.addWidget(self.ROI_groupbox)
        layout_controls.addLayout(layout_start_stop)
        layout_controls.addStretch()

        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(layout_controls)

    def set_timers(self):

        self.timer = QTimer()
        self.timer.timeout.connect(self.grab)
        self.timer.setInterval(33)
        self.timer.start()

    # Callbacks --------------------------------------------------------- 

    def closeEvent(self, event):
        self.stop_acquisition()

    def grab(self):
        # TODO this is probably not the right way to do it. First it is dictating
        # the FPS with the QT timer, and second it is consuming frames.
        # I should probably send frames from outside (with a queue or something)
        # and use the class only to control camera features.

        # NOTE I should be able to flush the queue when I change parameters 

        if self.acquisition_started:
            frame = self.camera.get_frame()
            self.image_label.setPixmap(NDarray_to_QPixmap(frame.image))

    def start_acquisition(self):
        if not self.acquisition_started:
            self.camera.start_acquisition()
            self.acquisition_started = True
            
    def stop_acquisition(self):
        if self.acquisition_started:
            self.camera.stop_acquisition()
            self.acquisition_started = False

    def set_exposure(self):
        self.camera.set_exposure(self.exposure_spinbox.value())

    def set_gain(self):
        self.camera.set_gain(self.gain_spinbox.value())

    def set_framerate(self):
        self.camera.set_framerate(self.framerate_spinbox.value())

    def set_offsetX(self):
        self.camera.set_offsetX(int(self.offsetX_spinbox.value()))

    def set_offsetY(self):
        self.camera.set_offsetY(int(self.offsetY_spinbox.value()))

    def set_width(self):
        self.camera.set_width(int(self.width_spinbox.value()))

    def set_height(self):
        self.camera.set_height(int(self.height_spinbox.value()))
       
