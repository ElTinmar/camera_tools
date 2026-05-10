from .camera import *
from .randomcam import *
from .zerocam import *
from .aravis import AravisCamera
from .ROI_sensor_widget import ROIGraphicalSelector

try:
    from .webcam import *
except ModuleNotFoundError:
    print('webcam not available')

# try:
#     from .webcam_v4l2 import *
# except ModuleNotFoundError:
#     print('v4l2 not available')

try:
    from .moviefilecam import *
except ModuleNotFoundError:
    print('moviefilecam not available')

try:
    from .calibration import get_camera_distortion, get_camera_px_per_mm
except ModuleNotFoundError:
    print('calibration not available')

try:
    from .ximeacam import *
except ModuleNotFoundError:
    print('module ximea not found, ximea cameras not available')
except OSError as e:
    print(f'OSError: {e}. Issue with ximea, try reinstalling XIMEA')


try:
    from .spinnaker import *
except ModuleNotFoundError:
    print('module spinnaker not found, spinnaker cameras not available')
except OSError as e:
    print(f'OSError: {e}. Issue with spinnaker, try reinstalling Spinnaker SDK')
