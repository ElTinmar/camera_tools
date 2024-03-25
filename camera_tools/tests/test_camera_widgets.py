import sys
from PyQt5.QtWidgets import QApplication
from camera_tools import CameraPreview, CameraControl
import numpy as np

if __name__ == '__main__':

    RANDOM = True
    WEBCAM = False
    XIMEA = False

    app = QApplication(sys.argv) 

    if RANDOM:
        from camera_tools import RandomCam
        cam = RandomCam(shape=(512,512), dtype=np.uint8)
        
    if WEBCAM:
        from camera_tools import OpenCV_Webcam
        cam = OpenCV_Webcam(-1)

    if XIMEA:
        from camera_tools import XimeaCamera
        cam = XimeaCamera()

    height = cam.get_height()
    width = cam.get_width()
    num_channel = cam.get_num_channels()
    bpp = cam.get_bit_depth()

    if num_channel == 1:
        shp = (height, width)
    else:
        shp = (height, width, num_channel)
    
    map = {
        8: np.uint8,
        16: np.uint16
    }
        
    image = np.zeros(shp, map[bpp])  
    
    controls = CameraControl(cam, image)
    window = CameraPreview(controls, image, display_fps=60)
    window.show()
    sys.exit(app.exec())

