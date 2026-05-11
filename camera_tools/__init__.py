import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

from .camera import Camera
from .calibration import get_camera_distortion, get_camera_px_per_mm
from .randomcam import RandomCam
from .zerocam import ZeroCam
from .ROI_sensor_widget import CameraSensorROI
from .moviefilecam import *
from .webcam import *

try:
    from .aravis import AravisCamera
except ModuleNotFoundError:
    logger.info('AravisCamera not available')
except OSError as e:
    logger.info(f'OSError: {e}. Issue with AravisCamera, try reinstalling aravis')

try:
    from .ximeacam import *
except ModuleNotFoundError:
    logger.info('module ximea not found, ximea cameras not available')
except OSError as e:
    logger.info(f'OSError: {e}. Issue with ximea, try reinstalling XIMEA')

try:
    from .spinnaker import *
except ModuleNotFoundError:
    logger.info('module spinnaker not found, spinnaker cameras not available')
except OSError as e:
    logger.info(f'OSError: {e}. Issue with spinnaker, try reinstalling Spinnaker SDK')
