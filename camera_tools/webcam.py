import cv2 
import time
from numpy.typing import NDArray
from camera_tools.camera import Camera
from typing import Optional, Tuple, Dict
import numpy as np
from image_tools import im2gray
import sys

# NOTE this is just a hack, OpenCV webacm control is very superficial 
# The right solution is probably to use v4l2 on linux
#   sudo apt install v4l-utils
#   v4l2-ctl -d /dev/video0 --list-formats-ext
#   v4l2-ctl -d /dev/video0 --list-ctrls-menus

# NOTE the constructor is very slow on windows (get_supported_configs)
# this also not very efficient on linux. Find a way to get supported
# format faster 

class OpenCV_Webcam(Camera):

    COMMON_RESOLUTIONS = [
        (320, 240),    # QVGA
        (640, 480),    # VGA
        (800, 600),    # SVGA
        (1024, 768),   # XGA
        (1280, 720),   # HD
        (1920, 1080),  # Full HD
        (3840, 2160),  # 4K
    ]

    COMMON_FRAMERATES = [5.0, 10.0, 15.0, 20.0, 24.0, 30.0, 60.0, 120.0]

    COMMON_FORMATS = {
        cv2.VideoWriter_fourcc(*"YUYV"): "YUYV",  # YUV 4:2:2
        cv2.VideoWriter_fourcc(*"YUY2"): "YUY2",  # 4:2:2
        #cv2.VideoWriter_fourcc(*"YV12"): "YV12",
        #cv2.VideoWriter_fourcc(*"NV12"): "NV12",
        #cv2.VideoWriter_fourcc(*"BGR3"): "BGR3",   
        #cv2.VideoWriter_fourcc(*"RGB3"): "RGB3",
        #cv2.VideoWriter_fourcc(*"GREY"): "GREY",
        #cv2.VideoWriter_fourcc(*"I420"): "I420",  
        cv2.VideoWriter_fourcc(*"MJPG"): "MJPG",  # Motion JPEG
    }

    def __init__(
            self, 
            cam_id: int = 0, 
            safe: bool = False,
            *args, 
            **kwargs
        ) -> None:
        
        super().__init__(*args, **kwargs)

        self.backend = cv2.CAP_DSHOW if sys.platform.startswith("win") else cv2.CAP_ANY 
        self.camera_id = cam_id
        self.safe = safe
        self.camera = cv2.VideoCapture(self.camera_id, self.backend) 
        self.index = 0
        self.time_start = time.perf_counter()
        self.supported_formats = {}
        self.supported_configs = {}
        self.supported_configs_list = []
        self.get_supported_configs()
        if self.supported_configs_list:
            self.current_config = self.supported_configs_list[-1]
            print(self.current_config)
            self.set_config(
                self.current_config['fourcc'],
                self.current_config['width'],
                self.current_config['height'],
                self.current_config['fps']
            )
        else:
            RuntimeError('No supported camera config found')

    def _reset(self):
        self.camera.release()
        self.camera = cv2.VideoCapture(self.camera_id, self.backend)
        self.index = 0
        self.time_start = time.perf_counter()
        self.set_config(
            self.current_config['fourcc'],
            self.current_config['width'],
            self.current_config['height'],
            self.current_config['fps']
        )

        # preallocate memory
        self.frame = np.empty((),
            dtype=np.dtype([
                ('index', int),
                ('timestamp', np.float64),
                ('image', np.uint8, (self.current_config['height'], self.current_config['width'], 3))
            ])
        )

    def start_acquisition(self) -> None:
        self._reset()

    def stop_acquisition(self) -> None:
        pass
    
    def set_config(self, fourcc: int, width: int, height: int, fps: float) -> None:
        self.camera.set(cv2.CAP_PROP_FOURCC, fourcc)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.camera.set(cv2.CAP_PROP_FPS, fps)
        self.camera.set(cv2.CAP_PROP_FOURCC, fourcc) # windows DSHOW 

    def get_config(self) -> Dict:
        fourcc = int(self.camera.get(cv2.CAP_PROP_FOURCC))
        width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.camera.get(cv2.CAP_PROP_FPS)
        format = self.COMMON_FORMATS.get(fourcc, 'unknown fourcc')
        return {'format': format, 'fourcc': fourcc, 'width': width, 'height': height, 'fps': fps}

    def get_supported_formats(self):
        for fourcc, format_name in self.COMMON_FORMATS.items():
            if self.camera.set(cv2.CAP_PROP_FOURCC, fourcc):
                self.supported_formats[fourcc] = format_name
    
    def get_supported_configs(self):
        self.get_supported_formats()
        for fourcc, format_name in self.supported_formats.items():
            for width, height in self.COMMON_RESOLUTIONS:
                valid_fps = []
                for fps in self.COMMON_FRAMERATES:
                    self.set_config(fourcc, width, height, fps)
                    config = self.get_config()

                    if (config['width'] == width and
                        config['height'] == height and
                        config['fps'] == fps and
                        config['fourcc'] == fourcc):
                        valid_fps.append(fps)
                        self.supported_configs_list.append(config)

                if valid_fps:
                    if format_name not in self.supported_configs:
                        self.supported_configs[format_name] = {}
                    if width not in self.supported_configs[format_name]:
                        self.supported_configs[format_name][width] = {}
                    self.supported_configs[format_name][width][height] = valid_fps
                
    def get_frame(self) -> NDArray:
        ret, img = self.camera.read()
        self.index += 1
        timestamp = time.perf_counter() - self.time_start

        self.frame['index'] = self.index
        self.frame['timestamp'] = timestamp
        self.frame['image'] = img[:,:,::-1] # bgr to rgb
        
        if self.safe:
            output = self.frame.copy()
        else:
            output = self.frame

        return output 
    
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
        if self.camera is not None:
            self.camera.set(cv2.CAP_PROP_FPS, fps)
        self.current_config = self.get_config()
       
    def get_framerate(self) -> Optional[float]:
        if self.camera is not None:
            return self.camera.get(cv2.CAP_PROP_FPS)

    def get_framerate_range(self) -> Optional[Tuple[float,float]]:
        config = self.get_config()
        valid_fps = self.supported_configs[config['format']][config['width']][config['height']]
        return (min(valid_fps), max(valid_fps))

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

    def get_offsetY_range(self) -> Optional[Tuple[int,int]]:
        pass

    def get_offsetY_increment(self) -> Optional[int]:
        pass

    def width_available(self) -> bool:
        return True
    
    def set_width(self, width: int) -> None:
        config = self.get_config()
        if width in self.supported_configs[config['format']].keys():
            valid_height = list(self.supported_configs[config['format']][width].keys())
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, valid_height[-1])
        self.current_config = self.get_config()

    def get_width(self) -> Optional[int]:
        return int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))

    def get_width_range(self) -> Optional[Tuple[int,int]]:
        config = self.get_config()
        valid_width = self.supported_configs[config['format']].keys()
        return (int(min(valid_width)), int(max(valid_width)))
    
    def get_width_increment(self) -> Optional[int]:
        return 2  

    def height_available(self) -> bool:
        return True
    
    def set_height(self, height) -> None:
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.current_config = self.get_config()
    
    def get_height(self) -> Optional[int]:
        return int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    def get_height_range(self) -> Optional[Tuple[int,int]]:
        config = self.get_config()
        valid_height = self.supported_configs[config['format']][config['width']].keys()
        return (int(min(valid_height)), int(max(valid_height)))

    def get_height_increment(self) -> Optional[int]:
        return 2 
    
    def get_num_channels(self):
        return 3
    
    def __del__(self):
        if self.camera is not None:
            self.camera.release()


class OpenCV_Webcam_InitEveryFrame(OpenCV_Webcam):

    # workaround to clear buffer and always get last frame. 
    # this is a bit slow 

    def get_frame(self) -> NDArray:
        
        self.start_acquisition()
        ret, img = self.camera.read()
        self.stop_acquisition()

        self.index += 1
        timestamp = time.perf_counter() - self.time_start

        self.frame['index'] = self.index
        self.frame['timestamp'] = timestamp
        self.frame['image'] = img[:,:,::-1] # bgr to rgb
        
        if self.safe:
            output = self.frame.copy()
        else:
            output = self.frame

        return output 

class OpenCV_Webcam_Gray(OpenCV_Webcam):

    def start_acquisition(self) -> None:
        self.camera.release()
        self.camera = cv2.VideoCapture(self.camera_id, self.backend)
        self.index = 0
        self.time_start = time.perf_counter()
        self.set_config(
            self.current_config['fourcc'],
            self.current_config['width'],
            self.current_config['height'],
            self.current_config['fps']
        )

        # preallocate memory
        self.frame = np.empty((),
            dtype=np.dtype([
                ('index', int),
                ('timestamp', np.float64),
                ('image', np.uint8, (self.current_config['height'], self.current_config['width']))
            ])
        )

    def get_frame(self):
        ret, img = self.camera.read()
        img_gray = im2gray(img)
        self.index += 1
        timestamp = time.perf_counter() - self.time_start

        self.frame['index'] = self.index
        self.frame['timestamp'] = timestamp
        self.frame['image'] = img_gray

        if self.safe:
            output = self.frame.copy()
        else:
            output = self.frame

        return output 

    def get_num_channels(self):
        return 1
    
class OpenCV_Webcam_LastFrame(OpenCV_Webcam):

    # workaround to clear buffer and always get last frame. 
    # constantly get images in a separate thread in a loop, 
    # and overwrite a single variable.
    pass

def get_cam_properties():
    VIDEO_CAPTURE_PROPERTIES = {
        0: "CAP_PROP_POS_MSEC",             # Current position of the video file in milliseconds
        1: "CAP_PROP_POS_FRAMES",           # Index of the next frame to be captured
        2: "CAP_PROP_POS_AVI_RATIO",        # Relative position of the video file: 0=start, 1=end
        3: "CAP_PROP_FRAME_WIDTH",          # Width of the frames in the video stream
        4: "CAP_PROP_FRAME_HEIGHT",         # Height of the frames in the video stream
        5: "CAP_PROP_FPS",                  # Frame rate
        6: "CAP_PROP_FOURCC",               # Codec four-character code
        7: "CAP_PROP_FRAME_COUNT",          # Number of frames in the video file
        8: "CAP_PROP_FORMAT",               # Format of the Mat object returned by VideoCapture::retrieve()
        9: "CAP_PROP_MODE",                 # Backend-specific value indicating the current capture mode
        10: "CAP_PROP_BRIGHTNESS",          # Brightness of the image (only for cameras)
        11: "CAP_PROP_CONTRAST",            # Contrast of the image (only for cameras)
        12: "CAP_PROP_SATURATION",          # Saturation of the image (only for cameras)
        13: "CAP_PROP_HUE",                 # Hue of the image (only for cameras)
        14: "CAP_PROP_GAIN",                # Gain of the image (only for cameras)
        15: "CAP_PROP_EXPOSURE",            # Exposure (only for cameras)
        16: "CAP_PROP_CONVERT_RGB",         # Boolean: images will be converted to RGB or not
        17: "CAP_PROP_WHITE_BALANCE_BLUE_U",# White balance - Blue/U
        18: "CAP_PROP_RECTIFICATION",       # Rectification flag for stereo cameras (note: only for stereo cameras)
        19: "CAP_PROP_MONOCHROME",          # Monochrome mode
        20: "CAP_PROP_SHARPNESS",           # Sharpness of the image
        21: "CAP_PROP_AUTO_EXPOSURE",       # Auto exposure mode
        22: "CAP_PROP_GAMMA",               # Gamma correction
        23: "CAP_PROP_TEMPERATURE",         # Temperature of the image
        24: "CAP_PROP_TRIGGER",             # Trigger
        25: "CAP_PROP_TRIGGER_DELAY",       # Delay for the trigger
        26: "CAP_PROP_WHITE_BALANCE_RED_V", # White balance - Red/V
        27: "CAP_PROP_ZOOM",                # Zoom level
        28: "CAP_PROP_FOCUS",               # Focus setting
        29: "CAP_PROP_GUID",                # GUID for the device (only for FireWire cameras)
        30: "CAP_PROP_ISO_SPEED",           # ISO speed
        32: "CAP_PROP_BACKLIGHT",           # Backlight compensation
        33: "CAP_PROP_PAN",                 # Pan setting
        34: "CAP_PROP_TILT",                # Tilt setting
        35: "CAP_PROP_ROLL",                # Roll setting
        36: "CAP_PROP_IRIS",                # Iris setting
        37: "CAP_PROP_SETTINGS",            # Pop up the camera settings window
        38: "CAP_PROP_BUFFERSIZE",          # Number of frames to buffer
        39: "CAP_PROP_AUTOFOCUS",           # Autofocus
        40: "CAP_PROP_SAR_NUM",             # Sample aspect ratio numerator
        41: "CAP_PROP_SAR_DEN",             # Sample aspect ratio denominator
        42: "CAP_PROP_BACKEND",             # Video backend (enum)
        43: "CAP_PROP_CHANNEL",             # Current capture channel
        44: "CAP_PROP_AUTO_WB",             # Auto white balance
        45: "CAP_PROP_WB_TEMPERATURE",      # White balance temperature
        46: "CAP_PROP_CODEC_PIXEL_FORMAT",  # Pixel format of the codec
        47: "CAP_PROP_BITRATE",             # Video bitrate
        48: "CAP_PROP_ORIENTATION_META",    # Orientation metadata
        49: "CAP_PROP_ORIENTATION_AUTO",    # Automatic orientation handling
        53: "CAP_PROP_OPEN_TIMEOUT_MSEC",   # Timeout for opening the capture device (in milliseconds)
        54: "CAP_PROP_READ_TIMEOUT_MSEC",   # Timeout for reading a frame (in milliseconds)
    }

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open video capture device.")
    else:
        properties = {}
        for prop_id, prop_name in VIDEO_CAPTURE_PROPERTIES.items():
            value = cap.get(prop_id)
            if value != -1:  # Property is supported
                properties[prop_name] = value
        cap.release()

        # Print supported properties and their current values
        print("Supported properties and their values:")
        for name, value in properties.items():
            print(f"{name}: {value}")