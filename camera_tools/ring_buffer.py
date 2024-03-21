from ipc_tools import MultiRingBuffer
from camera_tools.frame import BaseFrame, Frame
from numpy.typing import NDArray, ArrayLike, DTypeLike
import numpy as np
from typing import Optional

class FrameRingBuffer(MultiRingBuffer):

    def __init__(
            self, 
            num_items: int,
            frame_shape: ArrayLike, 
            frame_dtype: DTypeLike,
            t_refresh: float = 0.001,
            copy: bool = True
        ):

        super().__init__(
            num_items,
            item_shape = [[1],[1],frame_shape],
            data_type = [np.int64, np.float64, frame_dtype],
            t_refresh = t_refresh,
            copy = copy
        )

    def get(self, blocking: bool = True, timeout: float = float('inf')) -> Optional[Frame]:

        data = super().get(blocking, timeout)
        return BaseFrame(data[0].item(),data[1].item(),data[2])

    def put(self, frame: Frame) -> None:

        super().put([
            np.array(frame.index, dtype=np.int64), 
            np.array(frame.timestamp, dtype=np.float64), 
            frame.image
        ])
        