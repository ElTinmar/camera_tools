import sys
from PyQt5.QtWidgets import QApplication
from camera_tools import CameraPreview, CameraControl
import numpy as np

if __name__ == '__main__':

    RANDOM = False
    WEBCAM = True
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
    channel = cam.get_num_channels()
    bpp = cam.get_bit_depth()

    if channel == 2:
        shp = (height, width)
    elif channel == 3:
        shp = (height, width, channel)
    else:
        raise RuntimeError('invalid num channels')
    
    map = {
        8: np.uint8,
        16: np.uint16
    }
        
    image = np.zeros(shp, map[bpp])  
    
    controls = CameraControl(cam, image)
    window = CameraPreview(controls, image, display_fps=60)
    window.show()
    sys.exit(app.exec())

