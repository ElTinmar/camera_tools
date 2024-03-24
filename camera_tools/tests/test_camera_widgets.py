import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from camera_tools import (
    CameraPreview, RandomCam, CameraControl
)
import numpy as np

if __name__ == '__main__':

    app = QApplication(sys.argv) 
    image = np.zeros((512,512), dtype=np.uint8)    
    cam = RandomCam(shape=(512,512), dtype=np.uint8)
    controls = CameraControl(cam, image)
    window = CameraPreview(controls, image)
    window.show()
    sys.exit(app.exec())

