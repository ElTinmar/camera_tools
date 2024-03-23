import v4l2py 
import time
import cv2
import numpy as np
from numpy.typing import NDArray
from camera_tools.camera import Camera
from camera_tools.frame import BaseFrame
from typing import Optional, Tuple

class V4L2_Webcam(Camera):
    '''
    Available on linux only, uses a v4l2 python wrapper 
    '''

    def __init__(self, cam_id: int = 0, *args, **kwargs) -> None:
        
        super().__init__(*args, **kwargs)

        self.camera_id = cam_id
        self.camera = v4l2py.Device.from_id(self.camera_id) 
        self.camera.open()
        self.index = 0
        self.time_start = time.monotonic()

    def start_acquisition(self) -> None:
        self.camera.close()
        self.camera = v4l2py.Device.from_id(self.camera_id)
        self.camera.open()
        self.index = 0
        self.time_start = time.monotonic()

    def stop_acquisition(self) -> None:
        self.camera.close() 
    
    def get_frame(self) -> BaseFrame:
        frame = next(self.camera.__iter__())
        img = cv2.imdecode(np.frombuffer(frame.data,dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        return BaseFrame(frame.index, frame.timestamp, img)
    
    def set_exposure(self, exp_value: float) -> None:
        self.camera.controls.auto_exposure.value = 1
        self.camera.controls.exposure_time_absolute.value = exp_value
 
    def get_exposure(self) -> Optional[float]:
        return self.camera.controls.exposure_time_absolute.value

    def get_exposure_range(self) -> Optional[Tuple[float,float]]:
        minimum = self.camera.controls.exposure_time_absolute.minimum
        maximum = self.camera.controls.exposure_time_absolute.maximum
        return (minimum, maximum)

    def get_exposure_increment(self) -> Optional[float]:
        return self.camera.controls.exposure_time_absolute.step

    def set_framerate(self, fps: float) -> None:
        pass
       
    def get_framerate(self) -> Optional[float]:
        pass

    def get_framerate_range(self) -> Optional[Tuple[float,float]]:
        pass

    def get_framerate_increment(self) -> Optional[float]:
        pass

    def set_gain(self, gain: float) -> None:
        pass

    def get_gain(self) -> Optional[float]:
        pass

    def get_gain_range(self) -> Optional[Tuple[float,float]]:
        pass

    def get_gain_increment(self) -> Optional[float]:
        pass

    def set_ROI(self, left: int, bottom: int, height: int, width: int) -> None:
        pass

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
        pass

    def set_bit_depth(depth: int) -> None:
        pass
    
    def get_num_channels(self) -> Optional[int]:
        pass

    def set_num_channels(self, num_channels: int) -> None:
        pass
