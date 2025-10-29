import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="v4l2py")
from v4l2py.device import Device, BufferType 
import time
import numpy as np
from numpy.typing import NDArray
from camera_tools.camera import Camera
from typing import Optional, Tuple

'''
INFO Useful properties to probe
import v4l2py 

d = Device.from_id(0)
d.open()
d.controls
d.info
d.info.formats
d.info.frame_sizes 
(
   d.controls.brightness.minimum, 
   d.controls.brightness.maximum, 
   d.controls.brightness.step, 
   d.controls.brightness.value, 
   d.controls.brightness.is_writeable
) 
f = d.get_format(BufferType.VIDEO_CAPTURE)
(f.width, f.height)
'''

class V4L2_Webcam(Camera):
    '''
    Available on linux only, uses a v4l2 python wrapper 
    '''

    def __init__(self, cam_id: int = 0, *args, **kwargs) -> None:
        
        super().__init__(*args, **kwargs)

        self.camera_id = cam_id
        self.camera = Device.from_id(self.camera_id) 
        self.camera.open()
        self.index = 0
        self.time_start = time.perf_counter()

    def start_acquisition(self) -> None:
        self.camera.close()
        self.camera = Device.from_id(self.camera_id)
        self.camera.open()
        self.index = 0
        self.time_start = time.perf_counter()

    def stop_acquisition(self) -> None:
        self.camera.close() 
    
    def get_frame(self) -> NDArray:
        img = next(self.camera.__iter__())
        pixeldata = np.frombuffer(img.data, dtype=np.uint8)
        frame = np.array(
            (img.index, img.timestamp, pixeldata),
            dtype = np.dtype([
                ('index', int),
                ('timestamp', np.float32),
                ('image', pixeldata.dtype, pixeldata.shape)
            ])
        )
        return frame
    
    def exposure_available(self) -> bool:
        return self.camera.controls.exposure_time_absolute.is_writeable
    
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

    # TODO implement that
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
        return self.camera.controls.gain.is_writeable
    
    def set_gain(self, gain: float) -> None:
        self.camera.controls.gain.value = gain

    def get_gain(self) -> Optional[float]:
        return self.camera.controls.gain.value

    def get_gain_range(self) -> Optional[Tuple[float,float]]:
        return (self.camera.controls.gain.minimum, self.camera.controls.gain.maximum)

    def get_gain_increment(self) -> Optional[float]:
        return self.camera.controls.gain.step

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

    def get_num_channels(self):
        return 3