import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from camera_tools import (
    CameraPreview, RandomCam, CameraControl
)
import numpy as np

if __name__ == '__main__':

    USE_XIMEA = False

    app = QApplication(sys.argv)        
    
    if USE_XIMEA:
        from camera_tools import XimeaCamera
        cam = XimeaCamera(1)
    else:
        cam = RandomCam(shape=(512,512), dtype=np.uint8)

    controls = CameraControl(cam)
    window = CameraPreview(controls)
    window.show()
    sys.exit(app.exec())

