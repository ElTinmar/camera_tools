from camera_tools.camera import Camera
from typing import Optional, Tuple
from numpy.typing import NDArray
import numpy as np

import gi
gi.require_version ('Aravis', '0.10')
from gi.repository import Aravis

class AravisCamera(Camera):

    def __init__(self, dev_id: Optional[str] = None, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.dev_id = dev_id
        self.first_frame = True
        self.first_num = 0
        self.first_timestamp = 0
        self.num_buffers = 5
        
        # open camera
        self.cam = Aravis.Camera.new(dev_id)

        # basic config
        self.cam.set_acquisition_mode(Aravis.AcquisitionMode.CONTINUOUS)
        self.cam.set_frame_rate_enable(True)
        self.cam.set_exposure_time_auto(Aravis.Auto.OFF)
        self.cam.set_exposure_mode(Aravis.ExposureMode.TIMED)
        self.cam.set_gain_auto(Aravis.Auto.OFF)
        self.cam.set_pixel_format(Aravis.PIXEL_FORMAT_MONO_8)
        self.cam.set_binning(dx=1, dy=1)    

        self.stream = self.cam.create_stream(None, None)
        self.reallocate_buffers() 

    def reallocate_buffers(self) -> None:
        # TODO maybe I can allocate once in __init__ with sensor size
        payload = self.cam.get_payload()
        self.stream.delete_buffers()
        for i in range(self.num_buffers):
            self.stream.push_buffer(Aravis.Buffer.new_allocate(payload))

    def start_acquisition(self) -> None:
        self.cam.start_acquisition()
    
    def stop_acquisition(self) -> None:
        self.cam.stop_acquisition()

    def exposure_available(self) -> bool:
        return self.cam.is_exposure_time_available()

    def set_exposure(self, exp_time: float) -> None:
        self.cam.set_exposure_time(exp_time)

    def get_exposure(self) -> Optional[float]:
        return self.cam.get_exposure_time()

    def get_exposure_range(self) -> Optional[Tuple[float,float]]:
        bounds = self.cam.get_exposure_time_bounds()
        return (bounds.min, bounds.max)

    def get_exposure_increment(self) -> Optional[float]:
        return self.cam.get_exposure_time_increment()

    def framerate_available(self) -> bool:
        return self.cam.is_frame_rate_available()
    
    def set_framerate(self, fps: float) -> None:
        self.cam.set_frame_rate(fps)

    def get_framerate(self) -> Optional[float]:
        return self.cam.get_frame_rate()

    def get_framerate_range(self) -> Optional[Tuple[float,float]]:
        bounds = self.cam.get_frame_rate_bounds()
        return (bounds.min, bounds.max)

    def get_framerate_increment(self) -> Optional[float]:
        return self.cam.get_frame_rate_increment()

    def gain_available(self) -> bool:
        return self.cam.is_gain_available()
    
    def set_gain(self, gain: float) -> None:
        self.cam.set_gain(gain)

    def get_gain(self) -> Optional[float]:
        return self.cam.get_gain()

    def get_gain_range(self) -> Optional[Tuple[float,float]]:
        bounds = self.cam.get_gain_bounds()
        return (bounds.min, bounds.max)

    def get_gain_increment(self) -> Optional[float]:
        return self.cam.get_gain_increment()

    def ROI_available(self) -> bool:
        return self.cam.is_region_offset_available()
    
    def set_ROI(self, left: int, bottom: int, height: int, width: int) -> None:
        self.cam.set_region(x=left, y=bottom, width=width, height=height)
        self.reallocate_buffers()

    def get_ROI(self) -> Optional[Tuple[int,int,int,int]]:
        region = self.cam.get_region()
        return (region.x, region.y, region.height, region.width)

    def set_offsetX(self, offsetX: int) -> None:
        region = self.cam.get_region()
        self.cam.set_region(x=offsetX, y=region.y, width=region.width, height=region.height)
        self.reallocate_buffers()

    def offsetX_available(self) -> bool:
        return self.cam.is_region_offset_available()
    
    def get_offsetX(self) -> Optional[int]:
        region = self.cam.get_region()
        return region.x

    def get_offsetX_range(self) -> Optional[Tuple[int,int]]:
        bounds = self.cam.get_x_offset_bounds()
        return (bounds.min, bounds.max)

    def get_offsetX_increment(self) -> Optional[int]:
        return self.cam.get_x_offset_increment()

    def set_offsetY(self, offsetY: int) -> None:
        region = self.cam.get_region()
        self.cam.set_region(x=region.x, y=offsetY, width=region.width, height=region.height)
        self.reallocate_buffers()

    def offsetY_available(self) -> bool:
        return self.cam.is_region_offset_available()
    
    def get_offsetY(self) -> Optional[int]:
        region = self.cam.get_region()
        return region.y
    
    def get_offsetY_range(self) -> Optional[Tuple[int,int]]:
        bounds = self.cam.get_y_offset_bounds()
        return (bounds.min, bounds.max)

    def get_offsetY_increment(self) -> Optional[int]:
        return self.cam.get_y_offset_increment()

    def width_available(self) -> bool:
        return self.cam.is_region_offset_available()
    
    def set_width(self, width: int) -> None:
        region = self.cam.get_region()
        self.cam.set_region(x=region.x, y=region.y, width=width, height=region.height)
        self.reallocate_buffers()

    def get_width(self) -> Optional[int]:
        region = self.cam.get_region()
        return region.width

    def get_width_range(self) -> Optional[Tuple[int,int]]:
        bounds = self.cam.get_width_bounds()
        return (bounds.min, bounds.max)

    def get_width_increment(self) -> Optional[int]:
        return self.cam.get_width_increment()

    def height_available(self) -> bool:
        return self.cam.is_region_offset_available()
    
    def set_height(self, height: int) -> None:
        region = self.cam.get_region()
        self.cam.set_region(x=region.x, y=region.y, width=region.width, height=height)
        self.reallocate_buffers()
        
    def get_height(self) -> Optional[int]:
        region = self.cam.get_region()
        return region.height 
    
    def get_height_range(self) -> Optional[Tuple[int,int]]:
        bounds = self.cam.get_height_bounds()
        return (bounds.min, bounds.max)
    
    def get_height_increment(self) -> Optional[int]:
        return self.cam.get_height_increment()

    def get_frame(self) -> NDArray:

        buffer = self.stream.pop_buffer()
        h = buffer.get_image_height()
        w = buffer.get_image_width()
        raw_pixeldata = buffer.get_image_data()
        pixeldata = np.frombuffer(raw_pixeldata, np.uint8).reshape(h,w) # may need to copy
        im_num = buffer.get_frame_id()
        ts_nsec = buffer.get_timestamp()
        timestamp = ts_nsec*1e-9
        if self.first_frame:
            self.first_frame = False
            self.first_num = im_num
            self.first_timestamp = timestamp

        frame = np.array(
            (im_num-self.first_num, timestamp-self.first_timestamp, pixeldata),
            dtype = np.dtype([
                ('index', int),
                ('timestamp', np.float32),
                ('image', np.uint8, (h,w))
            ])
        )
                
        self.stream.push_buffer(buffer)
        return frame

    def get_num_channels(self) -> int:
        return 1
    

        
