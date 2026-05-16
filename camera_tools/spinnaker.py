from camera_tools.camera import Camera, CameraInfo
from typing import Optional, Tuple, List
import PySpin
from numpy.typing import NDArray
import numpy as np

class SpinnakerCamera(Camera):

    @classmethod
    def list_available_cameras(cls) -> List[CameraInfo]:
        ...

    def __init__(self, dev_id: int = 0, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.system = PySpin.System.GetInstance()
        self.cam_list = self.system.GetCameras()
        
        self.dev_id = dev_id
        self.first_frame = True
        self.first_num = 0
        self.first_timestamp = 0

        # open camera
        self.cam = self.cam_list[dev_id]
        self.cam.Init()

        # basic config
        self.cam.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)
        # self.cam.AcquisitionFrameRateEnable.SetValue(True) # not working ?
        self.cam.ExposureAuto.SetValue(PySpin.ExposureAuto_Off)
        self.cam.ExposureMode.SetValue(PySpin.ExposureMode_Timed)
        self.cam.GainAuto.SetValue(PySpin.GainAuto_Off)
        self.cam.PixelFormat.SetValue(PySpin.PixelFormat_Mono8)
        self.cam.TLStream.StreamBufferHandlingMode.SetValue(PySpin.StreamBufferHandlingMode_NewestOnly)

    def start_acquisition(self) -> None:
        self.cam.BeginAcquisition()
    
    def stop_acquisition(self) -> None:
        self.cam.EndAcquisition()

    def exposure_available(self) -> bool:
        return True

    def set_exposure(self, exp_time: float) -> None:
        self.cam.ExposureTime.SetValue(exp_time)

    def get_exposure(self) -> Optional[float]:
        return self.cam.ExposureTime.GetValue()

    def get_exposure_range(self) -> Optional[Tuple[float,float]]:
        exposure_min = self.cam.ExposureTime.GetMin()
        exposure_max = self.cam.ExposureTime.GetMax()
        return (exposure_min, exposure_max)

    def get_exposure_increment(self) -> Optional[float]:
        try:
            return self.cam.ExposureTime.GetInc()
        except PySpin.SpinnakerException:
            return 1.0

    def framerate_available(self) -> bool:
        return True
    
    def set_framerate(self, fps: float) -> None:
        try:
            self.cam.AcquisitionFrameRate.SetValue(fps)
        except PySpin.SpinnakerException: 
            pass

    def get_framerate(self) -> Optional[float]:
        return self.cam.AcquisitionFrameRate.GetValue()

    def get_framerate_range(self) -> Optional[Tuple[float,float]]:
        framerate_min = self.cam.AcquisitionFrameRate.GetMin()
        framerate_max = self.cam.AcquisitionFrameRate.GetMax()
        return (framerate_min, framerate_max)

    def get_framerate_increment(self) -> Optional[float]:
        try:
            return self.cam.AcquisitionFrameRate.GetInc()
        except PySpin.SpinnakerException:
            return 1.0

    def gain_available(self) -> bool:
        return True
    
    def set_gain(self, gain: float) -> None:
        self.cam.Gain.SetValue(gain)

    def get_gain(self) -> Optional[float]:
        return self.cam.Gain.GetValue()

    def get_gain_range(self) -> Optional[Tuple[float,float]]:
        gain_min = self.cam.Gain.GetMin()
        gain_max = self.cam.Gain.GetMax()
        return (gain_min, gain_max)

    def get_gain_increment(self) -> Optional[float]:
        try:
            return self.cam.Gain.GetInc()
        except PySpin.SpinnakerException:
            return 1.0

    def ROI_available(self) -> bool:
        return False
    
    def set_ROI(self, left: int, bottom: int, height: int, width: int) -> None:
        pass

    def get_ROI(self) -> Optional[Tuple[int,int,int,int]]:
        pass

    def set_offsetX(self, offsetX: int) -> None:
        try:
            self.cam.OffsetX.SetValue(int(offsetX))
        except PySpin.SpinnakerException:
            pass

    def offsetX_available(self) -> bool:
        return True
    
    def get_offsetX(self) -> Optional[int]:
        return self.cam.OffsetX.GetValue()

    def get_offsetX_range(self) -> Optional[Tuple[int,int]]:
        offsetX_min = self.cam.OffsetX.GetMin()
        offsetX_max = self.cam.OffsetX.GetMax()
        return (offsetX_min, offsetX_max)

    def get_offsetX_increment(self) -> Optional[int]:
        try:
            return self.cam.OffsetX.GetInc()
        except PySpin.SpinnakerException:
            return 1

    def set_offsetY(self, offsetY: int) -> None:
        try:
            self.cam.OffsetY.SetValue(int(offsetY))
        except PySpin.SpinnakerException:
            pass

    def offsetY_available(self) -> bool:
        return True
    
    def get_offsetY(self) -> Optional[int]:
        return self.cam.OffsetY.GetValue()

    def get_offsetY_range(self) -> Optional[Tuple[int,int]]:
        offsetY_min = self.cam.OffsetY.GetMin()
        offsetY_max = self.cam.OffsetY.GetMax()
        return (offsetY_min, offsetY_max)

    def get_offsetY_increment(self) -> Optional[int]:
        try:
            return self.cam.OffsetY.GetInc()
        except PySpin.SpinnakerException:
            return 1

    def width_available(self) -> bool:
        return True
    
    def set_width(self, width: int) -> None:
        try:
            self.cam.Width.SetValue(int(width))
        except PySpin.SpinnakerException:
            pass

    def get_width(self) -> Optional[int]:
        return self.cam.Width.GetValue()

    def get_width_range(self) -> Optional[Tuple[int,int]]:
        width_min = self.cam.Width.GetMin()
        width_max = self.cam.Width.GetMax()
        return (width_min, width_max)

    def get_width_increment(self) -> Optional[int]:
        try:
            return self.cam.Width.GetInc()
        except PySpin.SpinnakerException:
            return 1

    def height_available(self) -> bool:
        return True
    
    def set_height(self, height: int) -> None:
        try:
            self.cam.Height.SetValue(int(height))
        except PySpin.SpinnakerException:
            pass
        
    def get_height(self) -> Optional[int]:
        return self.cam.Height.GetValue()   
    
    def get_height_range(self) -> Optional[Tuple[int,int]]:
        height_min = self.cam.Height.GetMin()
        height_max = self.cam.Height.GetMax()
        return (height_min, height_max)
    
    def get_height_increment(self) -> Optional[int]:
        try:
            return self.cam.Height.GetInc()
        except PySpin.SpinnakerException:
            return 1

    def get_frame(self) -> NDArray:
        image_result = self.cam.GetNextImage()
        pixeldata = image_result.GetNDArray()

        im_num = image_result.GetFrameID()
        ts_nsec = image_result.GetTimeStamp()
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
                ('image', pixeldata.dtype, pixeldata.shape)
            ])
        )

        image_result.Release()
        return frame

    def get_num_channels(self) -> int:
        # TODO  imgdataformat = cam.get_imgdataformat()
        return 1

    def close(self) -> None:

        self.cam.DeInit()
        del self.cam
        self.cam = None
        self.cam_list.Clear()
        self.system.ReleaseInstance()

    def __del__(self) -> None:
        try:
            self.close()
        finally:
            self.cam = None

        
