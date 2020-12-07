import RPi.GPIO as GPIO
import cv2
import numpy as np
import picamera
from picamera import PiCamera
from picamera.array import PiRGBArray
import time

# image processing
# white 값. R: white~255, G: white~255, B:white~255 하얗게만듦.


def select_white(image, white):
    lower = np.uint8([white, white, white])
    upper = np.uint8([255, 255, 255])
    white_mask = cv2.inRange(image, lower, upper)
    return white_mask


camera = PiCamera()
camera.resolution = (320, 240)
camera.vflip = True
camera.hflip = True
camera.framerate = 30

# 해상도에 맞는 cv2 array 생성
rawCapture = PiRGBArray(camera, size=(320, 240))

time.sleep(.1)
t = time.time()

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # 이미지가 한장한장 array에 저장이 된다.
    image = frame.array
    mask_image = select_white(image, 70)
    cv2.imshow("Processed", mask_image)

    #cv2.imshow("Raw", image)

    key = cv2.waitKey(1) & 0xFF  # 에러 방지
    rawCapture.truncate(0)  # 에러 방지

    if key == ord('q'):
        break
