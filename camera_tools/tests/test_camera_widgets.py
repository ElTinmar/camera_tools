import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from camera_tools import (
    CameraPreview, RandomCam, XimeaCamera, CameraControl
)
import numpy as np

if __name__ == '__main__':

    USE_XIMEA = True

    app = QApplication(sys.argv)        
    
    if USE_XIMEA:
        cam = XimeaCamera(1)
    else:
        cam = RandomCam(shape=(512,512), dtype=np.uint8)

    controls = CameraControl(cam)
    window = CameraPreview(controls)
    window.show()
    sys.exit(app.exec())

