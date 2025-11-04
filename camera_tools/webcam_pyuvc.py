import uvc
from uvc.uvc_bindings import CameraMode
import numpy as np
from numpy.typing import NDArray
from camera_tools.camera import Camera
from typing import Optional, Tuple, Dict

class PyUVC_Webcam(Camera):

    def __init__(self, cam_index: int = 0, safe: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.safe = safe
        self.index = 0

        dev_list = uvc.device_list()
        if not dev_list:
            raise RuntimeError("No UVC devices found")

        if cam_index >= len(dev_list):
            raise RuntimeError(f"Camera index {cam_index} out of range")

        self.device_info = dev_list[cam_index]
        self.camera = uvc.Capture(self.device_info['uid'])
        self.set_mode(self.camera.available_modes[-1])

        # Preallocate frame storage
        self.frame = np.empty((),
            dtype=np.dtype([
                ('index', int),
                ('timestamp', np.float64),
                ('image', np.uint8, (self.camera.frame_mode.height, self.camera.frame_mode.width, 3))
            ])
        )

    def get_mode(self, format_name: str, width: int, height: int, fps: float) -> Optional[CameraMode]:
        for mode in self.camera.available_modes:
            if (mode.supported and
                mode.format_name == format_name and
                mode.width == width and
                mode.height == height and
                mode.fps == fps):
                return mode

    def set_mode(self, mode: CameraMode):
        self.camera.frame_mode = mode

    def set_config(self, format_name: str, width: int, height: int, fps: float):

        mode = self.get_mode(format_name, width, height, fps)
        if mode is None:
            return
        self.set_mode(mode)

    def get_config(self) -> Dict:
        width = self.camera.frame_mode.width
        height = self.camera.frame_mode.height
        fps = self.camera.frame_mode.fps
        fmt = self.camera.frame_mode.format_name
        return {'width': width, 'height': height, 'fps': fps, 'format': fmt}

    def start_acquisition(self):
        self.index = 0

    def stop_acquisition(self):
        self.camera.close()

    def get_frame(self) -> NDArray:
        frame = self.camera.get_frame()
        img = frame.rgb
        self.index += 1

        self.frame['index'] = self.index
        self.frame['timestamp'] = frame.timestamp
        self.frame['image'] = img

        if self.safe:
            return self.frame.copy()
        else:
            return self.frame

    # Exposure / gain controls
    def exposure_available(self) -> bool:
        return hasattr(self.camera, 'exposure')

    def set_exposure(self, exp_time: float):
        self.camera.exposure_auto = 1  # manual
        self.camera.exposure = exp_time

    def get_exposure(self) -> Optional[float]:
        return getattr(self.camera, 'exposure', None)

    def get_exposure_range(self) -> Optional[Tuple[float, float]]:
        if self.exposure_available():
            return (self.camera.exposure_min, self.camera.exposure_max)

    def gain_available(self) -> bool:
        return hasattr(self.camera, 'gain')

    def set_gain(self, gain: float):
        self.camera.gain = gain

    def get_gain(self) -> Optional[float]:
        return getattr(self.camera, 'gain', None)

    # Framerate access
    def framerate_available(self) -> bool:
        return True

    def set_framerate(self, fps: float):
        self.camera.frame_mode.fps = fps
        self.current_config = self.get_config()

    def get_framerate(self) -> Optional[float]:
        return self.camera.frame_mode.fps

    def get_num_channels(self):
        return 3

    # ROI
    def ROI_available(self) -> bool:
        return False

    def set_ROI(self, left: int, bottom: int, height: int, width: int) -> None:
        pass

    def get_ROI(self) -> Optional[Tuple[int,int,int,int]]:
        return None

    # Offsets
    def offsetX_available(self) -> bool:
        return False

    def set_offsetX(self, offsetX: int) -> None:
        pass

    def get_offsetX(self) -> Optional[int]:
        return None

    def get_offsetX_range(self) -> Optional[Tuple[int,int]]:
        return None

    def get_offsetX_increment(self) -> Optional[int]:
        return None

    def offsetY_available(self) -> bool:
        return False

    def set_offsetY(self, offsetY: int) -> None:
        pass

    def get_offsetY(self) -> Optional[int]:
        return None

    def get_offsetY_range(self) -> Optional[Tuple[int,int]]:
        return None

    def get_offsetY_increment(self) -> Optional[int]:
        return None

    # Width / Height
    def width_available(self) -> bool:
        return True

    def set_width(self, width: int) -> None:
        self.camera.frame_mode.width = width
        self.current_config = self.get_config()

    def get_width(self) -> Optional[int]:
        return self.camera.frame_mode.width

    def get_width_range(self) -> Optional[Tuple[int,int]]:
        widths = [c['width'] for c in self.supported_configs_list]
        return (min(widths), max(widths))

    def get_width_increment(self) -> Optional[int]:
        return 1

    def height_available(self) -> bool:
        return True

    def set_height(self, height: int) -> None:
        self.camera.frame_mode.height = height
        self.current_config = self.get_config()

    def get_height(self) -> Optional[int]:
        return self.camera.frame_mode.height

    def get_height_range(self) -> Optional[Tuple[int,int]]:
        heights = [c['height'] for c in self.supported_configs_list]
        return (min(heights), max(heights))

    def get_height_increment(self) -> Optional[int]:
        return 1

    # Framerate / Exposure / Gain increments / ranges
    def get_framerate_range(self) -> Optional[Tuple[float,float]]:
        fps_list = [c['fps'] for c in self.supported_configs_list]
        return (min(fps_list), max(fps_list))

    def get_framerate_increment(self) -> Optional[float]:
        return 1.0

    def get_exposure_increment(self) -> Optional[float]:
        return 1.0

    def get_gain_range(self) -> Optional[Tuple[float,float]]:
        if self.gain_available():
            return (self.camera.gain_min, self.camera.gain_max)
        return None

    def get_gain_increment(self) -> Optional[float]:
        return 1.0
