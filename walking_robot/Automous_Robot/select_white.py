import cv2
import numpy as np

#image processing
# white 값. R: white~255, G: white~255, B:white~255 하얗게만듦.
def select_white(image, white):
    lower = np.uint8([white, white, white])
    upper = np.uint8([255, 255, 255])
    white_mask = cv2.inRange(image, lower, upper)
    return white_mask