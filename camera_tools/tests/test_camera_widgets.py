import sys
from PyQt5.QtWidgets import QApplication
from camera_tools import (
    CameraPreview, CameraControl
)
import numpy as np

if __name__ == '__main__':

    USE_XIMEA = False
    USE_RANDOM = False
    USE_WEBCAM = True

    app = QApplication(sys.argv)        
    
    if USE_XIMEA:
        from camera_tools import XimeaCamera
        cam = XimeaCamera(1)

    if USE_RANDOM:
        from camera_tools import RandomCam
        cam = RandomCam(shape=(512,512), dtype=np.uint8)

    if USE_WEBCAM:
        from camera_tools import OpenCV_Webcam
        cam = OpenCV_Webcam()
        
    controls = CameraControl(cam)
    window = CameraPreview(controls)
    window.show()

    sys.exit(app.exec())

