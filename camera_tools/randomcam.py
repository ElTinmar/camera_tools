from camera_tools.camera import Camera
from camera_tools.frame import BaseFrame, Frame
import time
import numpy as np
from numpy.typing import NDArray, ArrayLike
from typing import Optional, Tuple

class RandomCam(Camera):
    """
    Provides a random image. This is just for testing
    """

    def __init__(self, shape: ArrayLike, dtype: np.dtype, *args, **kwargs):

        super().__init__(*args,**kwargs)

        self.img_count: int = 0
        self.time_start: float = time.monotonic()
        self.shape = shape 
        self.dtype = np.dtype(dtype)

    def get_frame(self) -> Frame:

        self.img_count += 1
        timestamp = time.monotonic() - self.time_start

        if np.issubdtype(self.dtype, np.integer):
            type_inf = np.iinfo(self.dtype)
            min_val = 0
            max_val = type_inf.max
            img = np.random.randint(min_val, max_val, self.shape, dtype=self.dtype)
        
        elif np.issubdtype(self.dtype, np.floating):
            img = np.random.uniform(0.0, 1.0, self.shape).astype(self.dtype)
        
        else:
            raise TypeError
        
        frame = BaseFrame(self.img_count, timestamp, img)
        return frame

    def start_acquisition(self) -> None:
        self.index = 0
        self.time_start = time.monotonic()

    def stop_acquisition(self) -> None:
        pass

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
        return self.shape[1]
    
    def get_width_range(self) -> Optional[int]:
        pass

    def get_width_increment(self) -> Optional[int]:
        pass 
    
    def set_height(self, height) -> None:
        pass
    
    def get_height(self) -> Optional[int]:
        return self.shape[0]    
    
    def get_height_range(self) -> Optional[int]:
        pass

    def get_height_increment(self) -> Optional[int]:
        pass 

    def get_bit_depth(self) -> Optional[int]:
        return 8*self.dtype.itemsize

    def set_bit_depth(depth: int) -> None:
        pass
