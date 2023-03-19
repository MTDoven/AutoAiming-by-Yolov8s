"""
This is a program based on Yolov8 for Autoaiming in shooting games.
Its superiority lies in the great breakthrough in speed.
    1. The latest torch 2.1.0 is used. (Though in windows, torch.compile() method cannot be used on Windows yet.)
    2. "mss" module is applied to achieve quick screen capture.
    3. The precompiled C module is implemented in the final data processing and simulation of mouse movement.
    4. It uses multiple threads to improve the running speed.
"""





""" Write Over Ultralytics """

# load some module from ultralytics
from ultralytics.yolo.data.dataloaders.stream_loaders import SourceTypes
from ultralytics.yolo.utils.torch_utils import smart_inference_mode
from ultralytics.yolo.v8.detect import DetectionPredictor
from ultralytics.yolo.cfg import get_cfg
from ultralytics.yolo.utils import ops
from ultralytics import YOLO
from Configure import *
import torch

# DetectionPredictor class is inherited and overwritten
class MyPredictor(DetectionPredictor):
    @smart_inference_mode() # with torch.no_grad():
    def stream_inference(self, source=None, model=None):
        im = torch.permute(torch.from_numpy(source),(2,0,1))[None].to(self.model.device)/255
        # numpy to torch; reshape to (1,3,640,640); 0-1 normalize;
        preds = self.model(im, augment=False, visualize=False)
        # The main part for inference
        pred = ops.non_max_suppression(preds, CONFIDENCE_BOUND, classes=self.args.classes)[0]
        # non-maximum suppression and get only one output. (CONFIDENCE_BOUND is set in Configure.py)
        pred[:, :4] = ops.scale_boxes(im.shape[2:], pred[:, :4], source.shape).round()
        # process the information
        callback(pred) # Do callback including mouse moving
        return [] # return None will cause a problem in the upper level function.

# YOLO class is inherited and overwritten
class MyYOLO(YOLO):
    @smart_inference_mode() # with torch.no_grad():
    def predict_warm_up(self, source=None):
        """
        This function will only be executed once, so don't worry about the running speed here
        Most of these are parameters that can be adjusted originally. But they are fixed here.
        If you think the change is necessary or beneficial, you can modify the corresponding parameters.
        """
        overrides = self.overrides.copy()
        overrides['conf'] = CONFIDENCE_BOUND
        overrides['mode'] = 'predict'
        overrides['save'] = False
        self.overrides.update(overrides)
        # update the overrides and save the parameters at the object
        self.task = overrides.get('task') or self.task
        self.predictor = MyPredictor(overrides=overrides)
        # Changed to MyDetectionPredictor. originally DetectionPredictor.
        self.predictor.setup_model(model=self.model, verbose=True)
        self.predictor.setup_source(source)
        self.predictor.model.warmup(imgsz=(1, 3, *self.predictor.imgsz))
        self.predictor.imgsz = [640, 640]
        # img size was set here, you may need to change it.
        self.predictor.source_type = SourceTypes(False, False, False, True)
        self.predictor.args = get_cfg(self.predictor.args, self.overrides)
        return self.predictor.predict_cli(source)





""" Main Part """

# Here are the main part for this assignment
from Callbacks import callback, timer
# callback will be called when finished inference
from keyboard import is_pressed
# HOT_KEY for inference or not was set in Configure.py. default: "alt"
import numpy as np
import threading
import time
import mss

# screenshot init
sec = mss.mss()
img = np.array(sec.grab(SCREEN_SHOT_BOX))[:,:,0:3]
# model init
model = MyYOLO(MODEL_NAME)
model.predict_warm_up(img)
# count_time init
count_time = 0
# lock init
lock1 = threading.Lock()
lock2 = threading.Lock()

# screenshot function for multiple threads
def screenshot():
    global img
    global count_time
    while True:
        # get lock1 first
        lock1.acquire()
        img_temp = np.array(sec.grab(SCREEN_SHOT_BOX))[:, :, 0:3]
        # SCREEN_SHOT_BOX was set in Configure.py
        img = img_temp.copy()
        # to avoid clash in variable img
        count_time += 1
        lock1.release()
        # get lock2 later
        lock2.acquire()
        img_temp = np.array(sec.grab(SCREEN_SHOT_BOX))[:, :, 0:3]
        # SCREEN_SHOT_BOX was set in Configure.py
        img = img_temp.copy()
        # to avoid clash in variable img
        count_time += 1
        lock2.release()

# inference function for multiple threads
def inference():
    while True:
        # get lock2 first
        lock2.acquire()
        if is_pressed(HOT_KEY): # HOT_KEY was set in Configure.py
            model.predictor.stream_inference(img)
        lock2.release()
        # get lock1 later
        lock1.acquire()
        if is_pressed(HOT_KEY): # HOT_KEY was set in Configure.py
            model.predictor.stream_inference(img)
        lock1.release()

# start main part
threading.Thread(target=screenshot, daemon=True).start()
threading.Thread(target=inference, daemon=True).start()





""" Time Recorder """

# Recording time and frame rate
time_last = time.time()
while True:
    if count_time >= REFRESH_FREQ:
        temp_print = time.time()-time_last
        count_time = 0
        time_last = time.time()
        timer(temp_print)
        # print the time or frame rate
        # timer is defined in Callback.py
    else:
        if is_pressed(HOT_KEY+"+esc"): break
        # Use alt+esc to exit
        time.sleep(0.005)
print("\nThe program exits.")