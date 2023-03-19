import pyautogui as pai
import mss
import time
sec = mss.mss()

img = pai.screenshot()
width, height = img.size
SCREEN_SHOT_BOX = (int(width/2-320), int(height/2-320),
                   int(width/2+320), int(height/2+320))

i = 000000
while True:
    i+=1
    time.sleep(0.5)
    img = sec.grab(SCREEN_SHOT_BOX)
    mss.tools.to_png(img.rgb, img.size, 6, f"../DataSet/images/{str(i).zfill(6)}.jpg")