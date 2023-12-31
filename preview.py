from camera_tools import RandomCam, OpenCV_Webcam, Frame_RingBuffer, XimeaCamera
from multiprocessing import Process, Event
import time
import cv2
import numpy as np
from queue import Empty

## parameters -----------------------------
# video preview
DISPLAY_FPS = 30
DISPLAY_SCALE = 0.5
# camera parameters
FPS = 100
EXPOSURE = 4000
GAIN = 4.0
WIDTH  = 2048
HEIGHT = 2048
# queue size monitor
MONITOR_RATE_HZ = 10
SLEEP_TIME_S = 0.01
## ------------------------------------------    

# open camera 
#cam = OpenCV_Webcam()
#cam = RandomCam(shape=(HEIGHT,WIDTH),dtype=np.uint8)
cam = XimeaCamera()

# get ROI parameters 
x_inc = cam.get_offsetX_increment()
y_inc = cam.get_offsetY_increment()
max_width = cam.get_offsetX_range()[1]+cam.get_width_range()[1]
max_height = cam.get_offsetY_range()[1]+cam.get_height_range()[1]
OFFSET_X = int((max_width-WIDTH)/(2*x_inc))*x_inc
OFFSET_Y = int((max_height-HEIGHT)/(2*y_inc))*y_inc

# configure camera
cam.set_exposure(EXPOSURE)
cam.set_framerate(FPS)
cam.set_gain(GAIN)
cam.set_width(WIDTH)
cam.set_height(HEIGHT)
cam.set_offsetX(OFFSET_X)
cam.set_offsetY(OFFSET_Y)

def monitor_queue_sizes(queue_display, stop: Event):
    while not stop.is_set():
        start = time.time()
        while time.time() - start < 1/MONITOR_RATE_HZ:
            time.sleep(SLEEP_TIME_S)
        print(f'Display: {queue_display.qsize()}', flush = True)

def display_image(queue_display, stop: Event):
    cv2.namedWindow('display')
    while not stop.is_set():
        try:
            data = queue_display.get()
            frame_small = cv2.resize(data.image, None, None, DISPLAY_SCALE, DISPLAY_SCALE)
            cv2.imshow('display', frame_small)
            if cv2.waitKey(1) == ord('q'):
                stop.set()
                break
        except Empty:
            pass

    cv2.destroyAllWindows()


queue_display = Frame_RingBuffer(
    num_items=100,
    frame_shape=(HEIGHT,WIDTH),
    frame_dtype=np.uint8,
    copy = False
)

stop = Event()
display = Process(target=display_image, args=(queue_display,stop))
monitor = Process(target=monitor_queue_sizes, args=(queue_display,stop))

monitor.start()
display.start()

# img.acq_nframe is one-indexed
cam.start_acquisition()
while not stop.is_set():
    try:
        # get image and metadata
        frame = cam.get_frame()
        if (frame.index*1000/FPS) % DISPLAY_FPS*1000 == 0:
            queue_display.put(frame)
    except:
        cam.stop_acquisition()
        display.join()
        monitor.join()
        break


