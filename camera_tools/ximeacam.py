from camera_tools.camera import Camera
from typing import Optional, Tuple
from ximea import xiapi
from numpy.typing import NDArray
import numpy as np

class XimeaCamera(Camera):

    def __init__(self, dev_id: int = 0, *args, **kwargs):

        super().__init__(*args, **kwargs)
        
        self.dev_id = dev_id
        self.first_frame = True
        self.first_num = 0
        self.first_timestamp = 0

        # open camera
        self.xi_cam = xiapi.Camera(dev_id)
        self.xi_cam.open_device()
        
        # create buffer 
        self.xi_img = xiapi.Image()

        self.cam_name = self.xi_cam.get_device_name()

        if (b'MQ' in self.cam_name) or (b'MD' in self.cam_name):
            self.xi_cam.set_acq_timing_mode('XI_ACQ_TIMING_MODE_FRAME_RATE')
        else:
            self.xi_cam.set_acq_timing_mode('XI_ACQ_TIMING_MODE_FRAME_RATE_LIMIT')        

        # retrive most recent frame
        #self.xi_cam.enable_recent_frame()
        
        # skip images if you dont process fast enough by reducing num images in buffer
        #self.xi_cam.set_buffers_queue_size(2)

        # disable image processing 
        self.xi_cam.set_imgdataformat('XI_RAW8') 

        # change buffer policy to avoid data copy
        self.xi_cam.set_buffer_policy('XI_BP_UNSAFE') 
        # this will probably require manual buffer management and a function
        # like get_frame(self, buffer) 
        
    def start_acquisition(self) -> None:
        self.xi_cam.start_acquisition()
    
    def stop_acquisition(self) -> None:
        self.xi_cam.stop_acquisition()

    def exposure_available(self) -> bool:
        return True

    def set_exposure(self, exp_time: float) -> None:
        self.xi_cam.set_exposure(exp_time)

    def get_exposure(self) -> Optional[float]:
        return self.xi_cam.get_exposure()

    def get_exposure_range(self) -> Optional[Tuple[float,float]]:
        exposure_min = self.xi_cam.get_exposure_minimum()
        exposure_max = self.xi_cam.get_exposure_maximum()
        return (exposure_min, exposure_max)

    def get_exposure_increment(self) -> Optional[float]:
        return self.xi_cam.get_exposure_increment()

    def framerate_available(self) -> bool:
        return True
    
    def set_framerate(self, fps: float) -> None:
        if fps == 0:
            self.xi_cam.set_acq_timing_mode('XI_ACQ_TIMING_MODE_FREE_RUN')
        else:
            if (b'MQ' in self.cam_name) or (b'MD' in self.cam_name):
                self.xi_cam.set_acq_timing_mode('XI_ACQ_TIMING_MODE_FRAME_RATE')
            else:
                self.xi_cam.set_acq_timing_mode('XI_ACQ_TIMING_MODE_FRAME_RATE_LIMIT')
            self.xi_cam.set_framerate(fps)

    def get_framerate(self) -> Optional[float]:
        return self.xi_cam.get_framerate()

    def get_framerate_range(self) -> Optional[Tuple[float,float]]:
        framerate_min = self.xi_cam.get_framerate_minimum()
        framerate_max = self.xi_cam.get_framerate_maximum()
        return (framerate_min, framerate_max)

    def get_framerate_increment(self) -> Optional[float]:
        return self.xi_cam.get_framerate_increment()

    def gain_available(self) -> bool:
        return True
    
    def set_gain(self, gain: float) -> None:
        self.xi_cam.set_gain(gain)

    def get_gain(self) -> Optional[float]:
        return self.xi_cam.get_gain()

    def get_gain_range(self) -> Optional[Tuple[float,float]]:
        gain_min = self.xi_cam.get_gain_minimum()
        gain_max = self.xi_cam.get_gain_maximum()
        return (gain_min, gain_max)

    def get_gain_increment(self) -> Optional[float]:
        return self.xi_cam.get_gain_increment()

    def ROI_available(self) -> bool:
        return False
    
    def set_ROI(self, left: int, bottom: int, height: int, width: int) -> None:
        try:
            self.set_width(width)
            self.set_height(height)
            self.set_offsetX(left)
            self.set_offsetY(bottom)
        except xiapi.Xi_error:
            pass

    def get_ROI(self) -> Optional[Tuple[int,int,int,int]]:
        pass

    def set_offsetX(self, offsetX: int) -> None:
        offsetX_min, offsetX_max = self.get_offsetX_range()
        offsetX_inc = self.get_offsetX_increment()

        closest_valid_offsetX = round(offsetX/offsetX_inc)*offsetX_inc
        clamped_offsetX = max(offsetX_min, min(offsetX_max, closest_valid_offsetX))
    
        try:
            self.xi_cam.set_offsetX(int(clamped_offsetX))
        except xiapi.Xi_error:
            pass

    def offsetX_available(self) -> bool:
        return True
    
    def get_offsetX(self) -> Optional[int]:
        return self.xi_cam.get_offsetX()

    def get_offsetX_range(self) -> Optional[Tuple[int,int]]:
        offsetX_min = self.xi_cam.get_offsetX_minimum()
        offsetX_max = self.xi_cam.get_offsetX_maximum()
        return (offsetX_min, offsetX_max)

    def get_offsetX_increment(self) -> Optional[int]:
        return self.xi_cam.get_offsetX_increment()

    def set_offsetY(self, offsetY: int) -> None:
        offsetY_min, offsetY_max = self.get_offsetY_range()
        offsetY_inc = self.get_offsetY_increment()

        closest_valid_offsetY = round(offsetY/offsetY_inc)*offsetY_inc
        clamped_offsetY = max(offsetY_min, min(offsetY_max, closest_valid_offsetY))

        try:
            self.xi_cam.set_offsetY(int(clamped_offsetY))
        except xiapi.Xi_error:
            pass

    def offsetY_available(self) -> bool:
        return True
    
    def get_offsetY(self) -> Optional[int]:
        return self.xi_cam.get_offsetY()

    def get_offsetY_range(self) -> Optional[Tuple[int,int]]:
        offsetY_min = self.xi_cam.get_offsetY_minimum()
        offsetY_max = self.xi_cam.get_offsetY_maximum()
        return (offsetY_min, offsetY_max)

    def get_offsetY_increment(self) -> Optional[int]:
        return self.xi_cam.get_offsetY_increment()

    def width_available(self) -> bool:
        return True
    
    def set_width(self, width: int) -> None:
        width_min, width_max = self.get_width_range()
        width_inc = self.get_width_increment()

        closest_valid_width = round(width/width_inc)*width_inc
        clamped_width = max(width_min, min(width_max, closest_valid_width))
        
        try:
            self.xi_cam.set_width(int(clamped_width))
        except xiapi.Xi_error:
            pass

    def get_width(self) -> Optional[int]:
        return self.xi_cam.get_width()

    def get_width_range(self) -> Optional[Tuple[int,int]]:
        width_min = self.xi_cam.get_width_minimum()
        width_max = self.xi_cam.get_width_maximum()
        return (width_min, width_max)

    def get_width_increment(self) -> Optional[int]:
        return self.xi_cam.get_width_increment()

    def height_available(self) -> bool:
        return True
    
    def set_height(self, height: int) -> None:
        height_min, height_max = self.get_height_range()
        height_inc = self.get_height_increment()

        closest_valid_height = round(height/height_inc)*height_inc
        clamped_height = max(height_min, min(height_max, closest_valid_height))
        
        try:
            self.xi_cam.set_height(int(clamped_height))
        except xiapi.Xi_error:
                pass
        
    def get_height(self) -> Optional[int]:
        return self.xi_cam.get_height()    
    
    def get_height_range(self) -> Optional[Tuple[int,int]]:
        height_min = self.xi_cam.get_height_minimum()
        height_max = self.xi_cam.get_height_maximum()
        return (height_min, height_max)
    
    def get_height_increment(self) -> Optional[int]:
        return self.xi_cam.get_height_increment()

    def get_frame(self) -> NDArray:
        self.xi_cam.get_image(self.xi_img)
        pixeldata = self.xi_img.get_image_data_numpy()
        im_num = self.xi_img.acq_nframe
        ts_sec = self.xi_img.tsSec
        ts_usec = self.xi_img.tsUSec
        timestamp = (ts_sec*1_000_000 +  ts_usec)/1_000_000
        if self.first_frame:
            self.first_frame = False
            self.first_num = im_num
            self.first_timestamp = timestamp

        frame = np.array(
            (im_num-self.first_num, timestamp-self.first_timestamp, pixeldata),
            dtype = np.dtype([
                ('index', int),
                ('timestamp', np.float32),
                ('image', pixeldata.dtype, pixeldata.shape)
            ])
        )
        return frame

    def get_num_channels(self):
        # TODO  imgdataformat = cam.get_imgdataformat()
        return 1
    
    def __del__(self):
        if self.xi_cam is not None:
            self.xi_cam.close_device()


class numpy_holder(object):
    pass

class XimeaCamera_Transport(XimeaCamera):
    '''
    Use XI_FRM_TRANSPORT_DATA to bypass any image processing
    done on image reception. Directly handle the memory buffer
    provided by the ximea api 
    '''

    def __init__(self, dev_id: int = 0, *args, **kwargs):

        super().__init__(dev_id, *args, **kwargs)
        self.xi_cam.set_imgdataformat('XI_FRM_TRANSPORT_DATA')
        self.image_holder = numpy_holder()

    def get_frame(self) -> NDArray:

        self.xi_cam.get_image(self.xi_img)

        buffer = {
            'data': (self.xi_img.bp, False),
            'strides': None,
            'descr': [('', '|u1')],
            'typestr': '|u1',
            'shape': (self.xi_img.height, self.xi_img.width),
            'version': 3
        }
        self.image_holder.__array_interface__ = buffer
        pixeldata = np.array(self.image_holder, copy=False)
        
        im_num = self.xi_img.acq_nframe
        ts_sec = self.xi_img.tsSec
        ts_usec = self.xi_img.tsUSec
        timestamp = (ts_sec*1_000_000 +  ts_usec)/1_000_000
        if self.first_frame:
            self.first_frame = False
            self.first_num = im_num
            self.first_timestamp = timestamp

        frame = np.array(
            (im_num-self.first_num, timestamp-self.first_timestamp, pixeldata),
            dtype = np.dtype([
                ('index', int),
                ('timestamp', np.float32),
                ('image', pixeldata.dtype, pixeldata.shape)
            ])
        )
        return frame