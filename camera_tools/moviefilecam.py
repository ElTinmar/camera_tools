from camera_tools.camera import Camera
from video_tools import InMemory_OpenCV_VideoReader, get_video_info
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

    def __init__(self, filename: str, fps:int = 60, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.img_count: int = 0
        self.time_start: float = time.monotonic()
        if not os.path.isfile(filename):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)
        self.filename = filename
        self.reader = None
        self.fps = fps
        self.prev_time = 0

    def start_acquisition(self) -> None:
        self.reader = cv2.VideoCapture(self.filename)

    def stop_acquisition(self) -> None:
        self.reader.release()

    def get_frame(self) -> Optional[NDArray]:
        if self.reader is not None:
            self.img_count += 1
            rval, img = self.reader.read()
            timestamp = time.monotonic() - self.time_start

            if self.fps == 0:
                frame = np.array(
                    (self.img_count, timestamp, img),
                    dtype = np.dtype([
                        ('index', int),
                        ('timestamp', np.float32),
                        ('image', img.dtype, img.shape)
                    ])
                )
                self.prev_time = timestamp
                return frame

            while timestamp - self.prev_time < 1/self.fps:
                time.sleep(0.005)
                timestamp = time.monotonic() - self.time_start
            self.prev_time = timestamp
            
            frame = np.array(
                (self.img_count, timestamp, img),
                dtype = np.dtype([
                    ('index', int),
                    ('timestamp', np.float32),
                    ('image', img.dtype, img.shape)
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
        return True
    
    def set_framerate(self, fps: float) -> None:
        self.fps = fps
    
    def get_framerate(self) -> Optional[float]:
        return self.fps

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
        return True
    
    def set_width(self, width: int) -> None:
        pass

    def get_width(self) -> Optional[int]:
        self.start_acquisition()
        width = self.reader.get(cv2.CAP_PROP_FRAME_WIDTH)    
        self.stop_acquisition()
        return int(width)

    def get_width_range(self) -> Optional[int]:
        width = self.get_width()
        return (width, width)

    def get_width_increment(self) -> Optional[int]:
        return 0 

    def height_available(self) -> bool:
        return True
    
    def set_height(self, height) -> None:
        pass
    
    def get_height(self) -> Optional[int]:
        self.start_acquisition()
        height = self.reader.get(cv2.CAP_PROP_FRAME_HEIGHT)    
        self.stop_acquisition()
        return int(height)
    
    def get_height_range(self) -> Optional[int]:
        height = self.get_height()
        return (height, height)

    def get_height_increment(self) -> Optional[int]:
        return 0 
    
    def get_num_channels(self) -> Optional[int]:
        return 3



class BufferedMovieFileCam(Camera):
    """
    Buffer video from file into memory. Useful to profile algorithm
    working on frames without being limitied by the speed of reading 
    from disk
    """

    def __init__(
            self, 
            filename: str, 
            memsize_bytes: int = 4e9, 
            safe: bool = False,
            single_precision: bool = False, 
            grayscale: bool = False,
            *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.img_count: int = 0
        if not os.path.isfile(filename):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)
        
        info = get_video_info(filename, safe)
        self.height = info["height"]
        self.width = info["width"]
        self.num_channels = info["num_channels"]
        self.fps = info["fps"]

        self.filename = filename
        self.memsize_bytes = memsize_bytes
        self.safe = safe
        self.single_precision = single_precision
        self.grayscale = grayscale 
        self.reader = InMemory_OpenCV_VideoReader()

    def start_acquisition(self) -> None:
        self.reader.open_file(
            filename = self.filename, 
            memsize_bytes = self.memsize_bytes, 
            safe = self.safe, 
            single_precision = self.single_precision, # WEIRD pre-converting to SP makes the loop slower ???
            grayscale = self.grayscale
        )

    def stop_acquisition(self) -> None:
        self.reader.close()

    def get_frame(self) -> Optional[NDArray]:
        if self.reader is not None:
            rval, img = self.reader.next_frame()
            if rval:
                self.img_count += 1

                frame = np.array(
                    (self.img_count, time.perf_counter(), img),
                    dtype = np.dtype([
                        ('index', int),
                        ('timestamp', np.float32),
                        ('image', img.dtype, img.shape)
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
        return True
    
    def set_framerate(self, fps: float) -> None:
        self.fps = fps
    
    def get_framerate(self) -> Optional[float]:
        return self.fps
    
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
        return True
    
    def set_width(self, width: int) -> None:
        pass

    def get_width(self) -> Optional[int]:
        return self.width

    def get_width_range(self) -> Optional[int]:
        return (self.width, self.width)

    def get_width_increment(self) -> Optional[int]:
        return 0 

    def height_available(self) -> bool:
        return True
    
    def set_height(self, height) -> None:
        pass
    
    def get_height(self) -> Optional[int]:
        return self.height
    
    def get_height_range(self) -> Optional[int]:
        return (self.height, self.height)

    def get_height_increment(self) -> Optional[int]:
        return 0 

    def get_bit_depth(self) -> Optional[int]:
        pass

    def set_bit_depth(depth: int) -> None:
        pass

    def get_num_channels(self) -> Optional[int]:
        return self.num_channels

    def set_num_channels(self, num_channels: int) -> None:
        pass
