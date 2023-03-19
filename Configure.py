import pyautogui as pai
img = pai.screenshot()
width, height = img.size
# Check the size of your screen

SCREEN_SHOT_BOX = (int(width/2-320), int(height/2-320), int(width/2+320), int(height/2+320))
# A range to crop on the screen.
MODEL_NAME = 'MyModel.pt'
# The path to your model, which should be accepted by Ultralytics' yolo
CONFIDENCE_BOUND = 0.60
# Ignore the object whose confidence is lower than this.
REFRESH_FREQ = 100
# The frequency to get some information and show it on your screen.
HOT_KEY = "alt"
