from camera_tools.camera import Camera
from camera_tools.frame import BaseFrame, Frame
import time
import numpy as np
from numpy.typing import NDArray
import cv2
from typing import Optional, Tuple
import os 
import errno

class MovieFileCam(Camera):
    """
    Reads video from file
    """

    def __init__(self, filename: str, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.img_count: int = 0
        self.time_start: float = time.monotonic()
        if not os.path.isfile(filename):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)
        self.filename = filename
        self.reader = None

    def start_acquisition(self) -> None:
        self.reader = cv2.VideoCapture(self.filename)

    def stop_acquisition(self) -> None:
        self.reader.release()

    def get_frame(self) -> Optional[Frame]:
        if self.reader is not None:
            self.img_count += 1
            timestamp = time.monotonic() - self.time_start
            rval, img = self.reader.read()
            frame = BaseFrame(self.img_count, timestamp, img)
            return frame
    
    def set_exposure(self, exp_time: float) -> None:
        pass

    def get_exposure(self) -> Optional[float]:
        pass

    def get_exposure_range(self) -> Optional[Tuple[float,float]]:
        pass

    def get_exposure_increment(self) -> Optional[float]:
        pass

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
        self.start_acquisition()
        width = self.reader.get(cv2.CAP_PROP_FRAME_WIDTH)    
        self.stop_acquisition()
        return int(width)

    def get_width_range(self) -> Optional[int]:
        pass

    def get_width_increment(self) -> Optional[int]:
        pass 

    def set_height(self, height) -> None:
        pass
    
    def get_height(self) -> Optional[int]:
        self.start_acquisition()
        height = self.reader.get(cv2.CAP_PROP_FRAME_HEIGHT)    
        self.stop_acquisition()
        return int(height)
    
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