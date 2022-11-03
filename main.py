# MacOS X
# from mss.darwin import MSS as mss

# Microsoft Windows
# from mss.windows import MSS as mss

# GNU/Linux
from mss.linux import MSS as mss
import cv2 
import numpy
from PIL import Image
import time


def find_head(head, img):
    w, h = head.shape
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    method = eval(methods[1]) 

    img2 = img.copy()

    result = cv2.matchTemplate(img2, head, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if method in (cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED):
        loaction = min_loc
    else:
        location = max_loc

    bottom_right = (location[0]+w, location[1]+h)
    return cv2.rectangle(img2, location, bottom_right, (0, 0, 255), 5)


def record_screen():
    head = cv2.imread('head.png', 0)
    sct = mss()

    # monitor = {"top": 40, "left": 0, "width": 800, "height": 640}

    monitor_number = 1
    mon = sct.monitors[monitor_number]
    # print(mon)

    # The screen part to capture
    monitor = {
        "top": mon["top"] + 300,  # 100px from the top
        "left": mon["left"] + 400,  # 100px from the left
        "width": 1300,
        "height": 600,
        "mon": monitor_number,
    }

    # Счетчик FPS
    new_frame_time, prev_frame_time, fps = 0, 0, 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    while True:
        screenshot = sct.grab(monitor)
        img = numpy.array(screenshot)
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Счетчик FPS
        new_frame_time = time.time()
        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time
        fps = int(fps)

        # Display FPS
        cv2.putText(img, str(fps), (7, 40), font, 1, (100, 255, 0), 0, cv2.LINE_AA)

        res = find_head(head, img)

        cv2.imshow('OpenCV', res)

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

    return fps

print('FPS', record_screen())
