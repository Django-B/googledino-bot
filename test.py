import numpy as np
import cv2
import time


img = cv2.imread('screen.png', 0)
template = cv2.imread('head.png', 0)


w, h = template.shape

methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

for meth in methods:
    img2 = img.copy()

    method = eval(meth)

    result = cv2.matchTemplate(img2, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(min_loc, max_loc)

    if method in (cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED):
        loaction = min_loc
    else:
        location = max_loc

    bottom_right = (location[0]+w, location[1]+h)

    cv2.rectangle(img2, location, bottom_right, (0, 0, 255), 1)
    cv2.imshow('Match', img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
