import time
import pyautogui
import cv2
import mss
import numpy as np
import win32gui
import win32con

WindowName = "Lordz.io - bot v0.0.1"
org = (700, 600)  # (x,y) text of fps
font = cv2.FONT_HERSHEY_SIMPLEX  # text font
fontScale = 1  # text scale
threshold = 0.7  # accuracy
color = (200, 0, 200)  # color text
thickness = 2
coin = cv2.imread('coin.jpg', 0)  # coin object
coordinates = ()  # tupple of coordinates


########################################

# The game should be in the upper left corner and have a size of 800px x 640px

# always top most
def AlwaysTop():
    hWnd = win32gui.FindWindow(None, WindowName)
    win32gui.SetWindowPos(hWnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                          win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)


# starts within 5 sec
time.sleep(5)

with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": 0, "left": 0, "width": 800, "height": 640}

    while "Screen capturing":
        last_time = time.time()
        img = np.array(sct.grab(monitor))  # grab screen

        # Display the picture
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert BGR to Gray
        res = cv2.matchTemplate(img, coin, cv2.TM_CCOEFF_NORMED)  # search template on image

        w, h = coin.shape[::-1]  # get size of coin.jpg
        loc = np.where(res >= threshold)  # filter  bigger accuracy object

        if not loc:
            coordinates = ()

        for index, pt in enumerate(zip(*loc[::-1])):
            if index == 0:
                coordinates = [pt[0], pt[1]]

        if coordinates:
            pyautogui.moveTo((coordinates[0], coordinates[1]))

        cv2.putText(img, format(round(1 / (time.time() - last_time))), org, font, fontScale, color, thickness)
        cv2.imshow(WindowName, img)
        AlwaysTop()

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

time.sleep(1)
