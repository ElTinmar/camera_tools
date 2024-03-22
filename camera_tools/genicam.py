from camera_tools.camera import Camera
from camera_tools.frame import Frame
from harvesters.core import Harvester
from numpy.typing import NDArray
from typing import Optional, Tuple

class FrameHarvesters(Frame):
    def __init__(self, buffer):
        self._buffer = buffer

    @property
    def index(self) -> int:
        return self._buffer.num

    @property
    def timestamp(self) -> float:
        return self._buffer.timestamp

    @property
    def image(self) -> NDArray:
        return self._buffer.payload.component[0].data

    def reallocate(self):
        """This is important to allow the camera to reuse the buffer"""
        self._buffer.queue()

class GenicamHarvesters(Camera):

    def __init__(self, gentl_producer, *args, **kwargs):
        """
        Open camera using the GenICam/GenTL API
        Inputs:
            gentl_producer: *.cti file from camera vendor     
        """

        super().__init__(*args, **kwargs)

        self.img_count: int = 0
        self._h = Harvester()
        self._h.add_file(gentl_producer)
        self._h.update()

        # discover cameras
        if ~self._h.device_info_list:
            RuntimeError('No camera found')
        else:
            print(f"Found {len(self._h.device_info_list)} devices")

        self._imAcq = self._h.create(self._camera_index)
        self._imAcq.num_buffers = self._num_buffers
        self.node_map = self._imAcq.remote_device.node_map
        self.available_features = dir(self.node_map)

    def set_exposure(self, exp_time: float) -> None:
        self.node_map.ExposureTime.value = exp_time

    def get_exposure(self, exp_time: float) -> Optional[float]:
        return self.node_map.ExposureTime.value 

    def get_exposure_range(self) -> Optional[Tuple[float,float]]:
        pass

    def get_exposure_increment(self) -> Optional[float]:
        pass

    def set_framerate(self, fps: float) -> None:
        self.node_map.AcquisitionFrameRate.value = fps

    def get_framerate(self, fps: float) -> Optional[float]:
        return self.node_map.AcquisitionFrameRate.value

    def get_framerate_range(self) -> Optional[Tuple[float,float]]:
        pass

    def get_framerate_increment(self) -> Optional[float]:
        pass

    def set_gain(self, gain: float) -> None:
        self.node_map.Gain.value = gain

    def get_gain(self, gain: float) -> Optional[float]:
        return self.node_map.Gain.value

    def get_gain_range(self) -> Optional[Tuple[float,float]]:
        pass

    def get_gain_increment(self) -> Optional[float]:
        pass

    def set_ROI(self, left: int, bottom: int, height: int, width: int) -> None:
        self.node_map.Width.value = width
        self.node_map.Height.value = height
        self.node_map.OffsetX.value = left
        self.node_map.OffsetY.value = bottom

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
        pass

    def get_width_range(self) -> Optional[int]:
        pass

    def get_width_increment(self) -> Optional[int]:
        pass 

    def set_height(self, height) -> None:
        pass
    
    def get_height(self) -> Optional[int]:
        pass    
    
    def get_height_range(self) -> Optional[int]:
        pass

    def get_height_increment(self) -> Optional[int]:
        pass 

    def get_bit_depth(self) -> Optional[int]:
        pass

    def set_bit_depth(depth: int) -> None:
        pass

    def start_acquisition(self):
        self._imAcq.start()

    def stop_acquisition(self):
        self._imAcq.stop()

    def get_frame(self) -> Frame:
        self.img_count += 1
        buf = FrameHarvesters(self._imAcq.fetch())
        return buf
    
    def __del__(self):
        print(self._imAcq.statistics)
        self._imAcq.destroy()
        self._h.reset()