from .camera import *
from .camera_widget import *
from .randomcam import *
from .zerocam import *
import setup_ximea
import setup_spinnaker

try:
    from .webcam import *
except ModuleNotFoundError:
    print('webcam not available')

try:
    from .webcam_v4l2 import *
except ModuleNotFoundError:
    print('v4l2 not available')

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
except OSError:
    print('issue with ximea, try reinstalling XIMEA')


try:
    from .spinnaker import *
except ModuleNotFoundError:
    print('module spinnaker not found, spinnaker cameras not available')
except OSError:
    print('issue with spinnaker, try reinstalling Spinnaker SDK')
