from camera_tools.camera import Camera
import time
import numpy as np
from numpy.typing import NDArray, ArrayLike
from typing import Optional, Tuple

class ZeroCam(Camera):
    """
    Provides an empty image. This is just for testing
    """

    def __init__(self, shape: ArrayLike, dtype: np.dtype, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.img_count: int = 0
        self.time_start: float = time.monotonic()
        self.shape = shape 
        self.dtype = dtype

    def start_acquisition(self) -> None:
        self.index = 0
        self.time_start = time.monotonic()

    def stop_acquisition(self) -> None:
        pass

    def get_frame(self) -> NDArray:

        self.img_count += 1
        timestamp = time.monotonic() - self.time_start
        img = np.zeros(self.shape, dtype=self.dtype)
        frame = np.array(
            (self.img_count, timestamp, img),
            dtype = np.dtype([
                ('index', int),
                ('timestamp', np.float32),
                ('image', self.dtype, self.shape)
            ])
        )
        return frame
    
    def exposure_available(self) -> bool:
        return False
    
    def set_exposure(self, exp_time: float) -> None:
        pass

    def get_exposure(self) -> Optional[float]:
        pass

    def get_exposure_range(self) -> Optional[Tuple[float,float]]:
        pass

    def get_exposure_increment(self) -> Optional[float]:
        pass

    def framerate_available(self) -> bool:
        return False
    
    def set_framerate(self, fps: float) -> None:
        pass
    
    def get_framerate(self) -> Optional[float]:
        pass

    def get_framerate_range(self) -> Optional[Tuple[float,float]]:
        pass

    def get_framerate_increment(self) -> Optional[float]:
        pass

    def gain_available(self) -> bool:
        return False

    def set_gain(self, gain: float) -> None:
        pass

    def get_gain(self) -> Optional[float]:
        pass

    def get_gain_range(self) -> Optional[Tuple[float,float]]:
        pass

    def get_gain_increment(self) -> Optional[float]:
        pass

    def ROI_available(self) -> bool:
        return False
    
    def set_ROI(self, left: int, bottom: int, height: int, width: int) -> None:
        pass

    def get_ROI(self) -> Optional[Tuple[int,int,int,int]]:
        pass

    def offsetX_available(self) -> bool:
        return False
        
    def set_offsetX(self, offsetX: int) -> None:
        pass

    def get_offsetX(self) -> Optional[int]:
        pass

    def get_offsetX_range(self) -> Optional[int]:
        pass

    def get_offsetX_increment(self) -> Optional[int]:
        pass

    def offsetY_available(self) -> bool:
        return False
    
    def set_offsetY(self, offsetY: int) -> None:
        pass

    def get_offsetY(self) -> Optional[int]:
        pass

    def get_offsetY_range(self) -> Optional[int]:
        pass

    def get_offsetY_increment(self) -> Optional[int]:
        pass

    def width_available(self) -> bool:
        return False
    
    def set_width(self, width: int) -> None:
        pass

    def get_width(self) -> Optional[int]:
        pass

    def get_width_range(self) -> Optional[int]:
        pass

    def get_width_increment(self) -> Optional[int]:
        pass 

    def height_available(self) -> bool:
        return False
    
    def set_height(self, height) -> None:
        pass
    
    def get_height(self) -> Optional[int]:
        pass    
    
    def get_height_range(self) -> Optional[int]:
        pass

    def get_height_increment(self) -> Optional[int]:
        pass 