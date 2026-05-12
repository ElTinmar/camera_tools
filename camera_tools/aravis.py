from camera_tools.camera import Camera
from typing import Optional, Tuple, List
from numpy.typing import NDArray
import numpy as np

import gi
gi.require_version ('Aravis', '0.10')
from gi.repository import Aravis

# TODO: might need to enforce gain/exposure/framerate increment

class AravisCamera(Camera):

    @staticmethod
    def list_available_cameras() -> List:
        Aravis.update_device_list()
        
        found_devices = []
        for i in range(Aravis.get_n_devices()):
            found_devices.append({
                "id": Aravis.get_device_id(i),
                "vendor": Aravis.get_device_vendor(i),
                "model": Aravis.get_device_model(i),
                "address": Aravis.get_device_address(i) # Useful for GigE debugging
            })
        return found_devices
    
    def __init__(self, dev_id: Optional[str] = None, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.dev_id = dev_id
        self.first_frame = True
        self.first_num = 0
        self.first_timestamp = 0
        self.num_buffers = 5
        self.acquisition_started = False
        self.stream = None
        
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

        self.reallocate_buffers() 

    def reallocate_buffers(self) -> None:
        payload = self.cam.get_payload()
        
        if self.stream is not None:
            self.stream.delete_buffers()
            self.stream = None

        self.stream = self.cam.create_stream(None, None)
        for i in range(self.num_buffers):
            self.stream.push_buffer(Aravis.Buffer.new_allocate(payload))

    def start_acquisition(self) -> None:
        if not self.acquisition_started:
            self.cam.start_acquisition()
            self.acquisition_started = True
    
    def stop_acquisition(self) -> None:
        if self.acquisition_started:
            self.cam.stop_acquisition()
            self.acquisition_started = False

    def _align_value(self, value: int, increment: int) -> int:
        if increment <= 1:
            return value
        return (value // increment) * increment
    
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
        try:
            inc = self.cam.get_gain_increment()
        except Exception as e:
            print(f"Could not get increment: {e}")
            inc = 1.0
        return inc

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
        try:
            inc = self.cam.get_frame_rate_increment()
        except Exception as e:
            print(f"Could not get increment: {e}")
            inc = 1.0
        return inc

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
        try:
            inc = self.cam.get_gain_increment()
        except Exception as e:
            print(f"Could not get increment: {e}")
            inc = 1.0
        return inc

    def ROI_available(self) -> bool:
        return self.cam.is_region_offset_available()
    
    def set_ROI(self, left: int, bottom: int, width: int, height: int) -> None:
        inc_x = self.get_offsetX_increment()
        inc_y = self.get_offsetY_increment()
        inc_w = self.get_width_increment()
        inc_h = self.get_height_increment()

        a_left = self._align_value(left, inc_x)
        a_bottom = self._align_value(bottom, inc_y)
        a_width = self._align_value(width, inc_w)
        a_height = self._align_value(height, inc_h)

        self.cam.set_region(0, 0, a_width, a_height)
        self.cam.set_region(a_left, a_bottom, a_width, a_height)
        
        self.reallocate_buffers()

    def get_ROI(self) -> Optional[Tuple[int,int,int,int]]:
        region = self.cam.get_region()
        return (region.x, region.y, region.height, region.width)

    def set_offsetX(self, offsetX: int) -> None:
        r = self.cam.get_region()
        self.set_ROI(offsetX, r.y, r.width, r.height)

    def offsetX_available(self) -> bool:
        return self.cam.is_region_offset_available()
    
    def get_offsetX(self) -> Optional[int]:
        region = self.cam.get_region()
        return region.x

    def get_offsetX_range(self) -> Optional[Tuple[int,int]]:
        bounds = self.cam.get_x_offset_bounds()
        return (bounds.min, bounds.max)

    def get_offsetX_increment(self) -> Optional[int]:
        try:
            inc = self.cam.get_x_offset_increment()
        except Exception as e:
            print(f"Could not get increment: {e}")
            inc = 1
        return inc

    def set_offsetY(self, offsetY: int) -> None:
        r = self.cam.get_region()
        self.set_ROI(r.x, offsetY, r.width, r.height)

    def offsetY_available(self) -> bool:
        return self.cam.is_region_offset_available()
    
    def get_offsetY(self) -> Optional[int]:
        region = self.cam.get_region()
        return region.y
    
    def get_offsetY_range(self) -> Optional[Tuple[int,int]]:
        bounds = self.cam.get_y_offset_bounds()
        return (bounds.min, bounds.max)

    def get_offsetY_increment(self) -> Optional[int]:
        try:
            inc = self.cam.get_y_offset_increment()
        except Exception as e:
            print(f"Could not get increment: {e}")
            inc = 1
        return inc

    def width_available(self) -> bool:
        return self.cam.is_region_offset_available()
    
    def set_width(self, width: int) -> None:
        r = self.cam.get_region()
        self.set_ROI(r.x, r.y, width, r.height)

    def get_width(self) -> Optional[int]:
        region = self.cam.get_region()
        return region.width

    def get_width_range(self) -> Optional[Tuple[int,int]]:
        bounds = self.cam.get_width_bounds()
        return (bounds.min, bounds.max)

    def get_width_increment(self) -> Optional[int]:
        try:
            inc = self.cam.get_width_increment()
        except Exception as e:
            print(f"Could not get increment: {e}")
            inc = 1
        return inc

    def height_available(self) -> bool:
        return self.cam.is_region_offset_available()
    
    def set_height(self, height: int) -> None:
        r = self.cam.get_region()
        self.set_ROI(r.x, r.y, r.width, height)
        
    def get_height(self) -> Optional[int]:
        region = self.cam.get_region()
        return region.height 
    
    def get_height_range(self) -> Optional[Tuple[int,int]]:
        bounds = self.cam.get_height_bounds()
        return (bounds.min, bounds.max)
    
    def get_height_increment(self) -> Optional[int]:
        try:
            inc = self.cam.get_height_increment()
        except Exception as e:
            print(f"Could not get increment: {e}")
            inc = 1
        return inc

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
    
    def close(self) -> None:
        if self.cam is not None and self.acquisition_started:
            self.stop_acquisition()
        self.stream = None
        self.cam = None

    def __del__(self) -> None:
        try:
            self.close()
        finally:
            self.stream = None
            self.cam = None