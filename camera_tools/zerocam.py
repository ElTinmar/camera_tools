from camera_tools.camera import Camera
import time
import numpy as np
from numpy.typing import NDArray, ArrayLike
from typing import Optional, Tuple

class ZeroCam(Camera):
    """
    Provides an empty image. This is just for testing
    """

    def __init__(self, shape: ArrayLike, dtype: np.dtype, framerate: float = 30, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.img_count: int = 0
        self.time_start: float = time.perf_counter()
        self.shape = np.asarray(shape) 
        self.dtype = np.dtype(dtype)
        self.framerate = framerate

    def start_acquisition(self) -> None:
        self.index = 0
        self.time_start = time.perf_counter()

    def stop_acquisition(self) -> None:
        pass

    def get_frame(self) -> NDArray:

        timestamp = time.perf_counter() - self.time_start
        self.img_count += 1
        img = np.zeros(self.shape, dtype=self.dtype)
        frame = np.array(
            (self.img_count, timestamp, img),
            dtype = np.dtype([
                ('index', int),
                ('timestamp', np.float32),
                ('image', self.dtype, self.shape)
            ])
        )
        time.sleep(max(0, 1/self.framerate - (time.perf_counter() - timestamp)))
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
        return True
    
    def set_framerate(self, fps: float) -> None:
        self.framerate = fps
    
    def get_framerate(self) -> Optional[float]:
        return self.framerate

    def get_framerate_range(self) -> Optional[Tuple[float,float]]:
        return (1,1000)

    def get_framerate_increment(self) -> Optional[float]:
        return 1

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

    def get_offsetX_range(self) -> Optional[Tuple[int,int]]:
        pass

    def get_offsetX_increment(self) -> Optional[int]:
        pass

    def offsetY_available(self) -> bool:
        return False
    
    def set_offsetY(self, offsetY: int) -> None:
        pass

    def get_offsetY(self) -> Optional[int]:
        pass

    def get_offsetY_range(self) ->  Optional[Tuple[int,int]]:
        pass

    def get_offsetY_increment(self) -> Optional[int]:
        pass

    def width_available(self) -> bool:
        return True
    
    def set_width(self, width: int) -> None:
        self.shape[1] = width

    def get_width(self) -> Optional[int]:
        return self.shape[1]

    def get_width_range(self) -> Optional[Tuple[int,int]]:
        return (1,4096)

    def get_width_increment(self) -> Optional[int]:
        return 1 

    def height_available(self) -> bool:
        return True
    
    def set_height(self, height) -> None:
        self.shape[0] = height
    
    def get_height(self) -> Optional[int]:
        return self.shape[0]    
    
    def get_height_range(self) -> Optional[Tuple[int,int]]:
        return (1,4096)

    def get_height_increment(self) -> Optional[int]:
        return 1  
    
    def get_num_channels(self):
        if len(self.shape) == 3:
            num_channels = self.shape[2]
        else:
            num_channels = 1
        return num_channels