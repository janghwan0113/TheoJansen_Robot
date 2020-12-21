from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import cv2
from select_white import select_white
from set_path import set_path
from detect_stop import detect_stop
from AR_marker import AR_marker
from ultra_sonic import ultra_sonic

camera = PiCamera()
camera.resolution = (320, 240)
camera.vflip = True
camera.hflip = True
camera.framerate = 30

# 해상도에 맞는 cv2 array 생성
rawCapture = PiRGBArray(camera, size=(320, 240))

time.sleep(.1)
t = time.time()

# main()
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    image = frame.array
    mask_image = select_white(image, 120)  # mask image array

    # print(mask_image[150:160,140:180].mean())
    #detect_stop(image)
    set_path(mask_image, 0.04, image)
    # AR_marker(image)
    # ultra_sonic()
    cv2.imshow("Processed", mask_image)
    #cv2.imshow("Raw", image)

    key = cv2.waitKey(1) & 0xFF  # 에러 방지
    rawCapture.truncate(0)  # 에러 방지

    if key == ord('q'):
        break
