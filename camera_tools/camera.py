from abc import ABC, abstractmethod
from typing import Optional, Tuple
from numpy.typing import NDArray

# TODO add methods for binning / decimation
# __init__ and __del__ acquire and release camera lock respectively
 
class Camera(ABC):

    @abstractmethod
    def start_acquisition(self):
        pass

    @abstractmethod
    def stop_acquisition(self):
        pass

    @abstractmethod
    def get_frame(self) -> NDArray:
        pass

    @abstractmethod
    def exposure_available(self) -> bool:
        pass

    @abstractmethod
    def set_exposure(self, exp_time: float) -> None:
        pass

    @abstractmethod
    def get_exposure(self) -> Optional[float]:
        pass

    @abstractmethod
    def get_exposure_range(self) -> Optional[Tuple[float,float]]:
        pass

    @abstractmethod
    def get_exposure_increment(self) -> Optional[float]:
        pass

    @abstractmethod
    def framerate_available(self) -> bool:
        pass

    @abstractmethod
    def set_framerate(self, fps: float) -> None:
        pass

    @abstractmethod
    def get_framerate(self) -> Optional[float]:
        pass

    @abstractmethod
    def get_framerate_range(self) -> Optional[Tuple[float,float]]:
        pass

    @abstractmethod
    def get_framerate_increment(self) -> Optional[float]:
        pass

    @abstractmethod
    def gain_available(self) -> bool:
        pass

    @abstractmethod
    def set_gain(self, gain: float) -> None:
        pass

    @abstractmethod
    def get_gain(self) -> Optional[float]:
        pass

    @abstractmethod
    def get_gain_range(self) -> Optional[Tuple[float,float]]:
        pass

    @abstractmethod
    def get_gain_increment(self) -> Optional[float]:
        pass

    @abstractmethod
    def ROI_available(self) -> bool:
        pass

    @abstractmethod
    def set_ROI(self, left: int, bottom: int, height: int, width: int) -> None:
        pass

    @abstractmethod
    def get_ROI(self) -> Optional[Tuple[int,int,int,int]]:
        pass

    @abstractmethod
    def offsetX_available(self) -> bool:
        pass

    @abstractmethod
    def set_offsetX(self, offsetX: int) -> None:
        pass

    @abstractmethod
    def get_offsetX(self) -> Optional[int]:
        pass

    @abstractmethod
    def get_offsetX_range(self) -> Optional[Tuple[int,int]]:
        pass

    @abstractmethod
    def get_offsetX_increment(self) -> Optional[int]:
        pass

    @abstractmethod
    def offsetY_available(self) -> bool:
        pass

    @abstractmethod
    def set_offsetY(self, offsetY: int) -> None:
        pass

    @abstractmethod
    def get_offsetY(self) -> Optional[int]:
        pass

    @abstractmethod
    def get_offsetY_range(self) -> Optional[Tuple[int,int]]:
        pass

    @abstractmethod
    def get_offsetY_increment(self) -> Optional[int]:
        pass

    @abstractmethod
    def width_available(self) -> bool:
        pass

    @abstractmethod
    def set_width(self, width: int) -> None:
        pass

    @abstractmethod
    def get_width(self) -> Optional[int]:
        pass

    @abstractmethod
    def get_width_range(self) -> Optional[Tuple[int,int]]:
        pass

    @abstractmethod
    def get_width_increment(self) -> Optional[int]:
        pass

    @abstractmethod
    def height_available(self) -> bool:
        pass

    @abstractmethod
    def set_height(self, height) -> None:
        pass

    @abstractmethod
    def get_height(self) -> Optional[int]:
        pass    

    @abstractmethod
    def get_height_range(self) -> Optional[Tuple[int,int]]:
        pass

    @abstractmethod
    def get_height_increment(self) -> Optional[int]:
        pass

    @abstractmethod
    def get_num_channels(self) -> Optional[int]:
        pass
