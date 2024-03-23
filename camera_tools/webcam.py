import cv2 
import time
from numpy.typing import NDArray
from camera_tools.camera import Camera
from camera_tools.frame import BaseFrame
from typing import Optional, Tuple

# NOTE another option on linux is to use v4l2-ctl to change camera settings 
  
class OpenCV_Webcam(Camera):

    def __init__(self, cam_id: int = 0, *args, **kwargs) -> None:
        
        super().__init__(*args, **kwargs)

        self.camera_id = cam_id
        self.camera = cv2.VideoCapture(self.camera_id) 
        self.index = 0
        self.time_start = time.monotonic()

    def start_acquisition(self) -> None:
        self.camera.release()
        self.camera = cv2.VideoCapture(self.camera_id)
        self.index = 0
        self.time_start = time.monotonic()

    def stop_acquisition(self) -> None:
        self.camera.release() 
    
    def get_frame(self) -> BaseFrame:
        ret, frame = self.camera.read()
        self.index += 1
        timestamp = time.monotonic() - self.time_start
        return BaseFrame(self.index, timestamp, frame)
    
    def set_exposure(self, exp_time: float) -> None:
        if self.camera is not None:
            self.camera.set(cv2.CAP_PROP_EXPOSURE, exp_time)
 
    def get_exposure(self) -> Optional[float]:
        if self.camera is not None:
            return self.camera.get(cv2.CAP_PROP_EXPOSURE)

    def get_exposure_range(self) -> Optional[Tuple[float,float]]:
        pass

    def get_exposure_increment(self) -> Optional[float]:
        pass

    def set_framerate(self, fps: float) -> None:
        if self.camera is not None:
            self.camera.set(cv2.CAP_PROP_FPS, fps)
       
    def get_framerate(self) -> Optional[float]:
        if self.camera is not None:
            return self.camera.get(cv2.CAP_PROP_FPS)

    def get_framerate_range(self) -> Optional[Tuple[float,float]]:
        pass

    def get_framerate_increment(self) -> Optional[float]:
        pass

    def set_gain(self, gain: float) -> None:
        if self.camera is not None:
            self.camera.set(cv2.CAP_PROP_GAIN, gain)

    def get_gain(self) -> Optional[float]:
        if self.camera is not None:
            return self.camera.get(cv2.CAP_PROP_GAIN)

    def get_gain_range(self) -> Optional[Tuple[float,float]]:
        pass

    def get_gain_increment(self) -> Optional[float]:
        pass

    def set_ROI(self, left: int, bottom: int, height: int, width: int) -> None:
        if self.camera is not None:
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def get_ROI(self) -> Optional[Tuple[int,int,int,int]]:
        pass

    def set_offsetX(self, offsetX: int) -> None:
        pass

    def get_offsetX(self) -> Optional[int]:
        pass

    def get_offsetX_range(self) -> Optional[int]:
        pass

    def get_offsetX_increment(self) -> Optional[int]:
        pass

    def set_offsetY(self, offsetY: int) -> None:
        pass

    def get_offsetY(self) -> Optional[int]:
        pass

    def get_offsetY_range(self) -> Optional[int]:
        pass

    def get_offsetY_increment(self) -> Optional[int]:
        pass

    def set_width(self, width: int) -> None:
        pass

    def get_width(self) -> Optional[int]:
        pass

    def get_width_range(self) -> Optional[int]:
        pass

    def get_width_increment(self) -> Optional[int]:
        pass 

    def set_height(self, height) -> None:
        pass
    
    def get_height(self) -> Optional[int]:
        pass    
    
    def get_height_range(self) -> Optional[int]:
        pass

    def get_height_increment(self) -> Optional[int]:
        pass 

    def get_bit_depth(self) -> Optional[int]:
        format = int(self.camera.get(cv2.CAP_PROP_FORMAT))
        mapping = {
            cv2.CV_8U: 8,
            cv2.CV_16U: 16
        }
        return mapping[format]

    def set_bit_depth(depth: int) -> None:
        pass