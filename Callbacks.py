import numpy as np
# numpy ctype initiate
from Configure import *
import numpy.ctypeslib as npct
clib = npct.load_library("CFunctions.dll", ".")
clib.callback.argtypes = [npct.ndpointer(dtype=np.float32, ndim=2, flags="C_CONTIGUOUS")]

# init number of object
temp_information = 0

# callback function to move mouse
def callback(pred):
    # process and callback
    pred_numpy = pred.cpu().numpy()
    pad_bottom = np.zeros((8-(pred_numpy.shape[0]),6),dtype=np.float32)
    clib.callback(np.concatenate((pred_numpy,pad_bottom),axis=0))
    # record the number of object
    global temp_information
    temp_information = pred_numpy.shape[0]

# for print some information
def timer(timee):
    number_string = " %.3f"%(REFRESH_FREQ/timee)
    if len(number_string)==7: number_string = " "+number_string;
    print(f"\033c Frames per second:{number_string}\n"+
          f" There are {temp_information} objects in the view.")

