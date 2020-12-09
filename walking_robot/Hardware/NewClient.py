import RPi.GPIO as GPIO
import cv2
import numpy as np
import picamera
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
from http.client import HTTPConnection
import argparse
from socket import *
import atexit
from matplotlib import pyplot as plt

# 수동제어 관련 라이브러리
import json
from time import sleep
from Time import Time
from sys import argv


host = '192.168.1.5:8000'
PORT = 8000

# image processing
# white 값. R: white~255, G: white~255, B:white~255 하얗게만듦.


def select_white(image, white):
    lower = np.uint8([white, white, white])
    upper = np.uint8([255, 255, 255])
    white_mask = cv2.inRange(image, lower, upper)
    return white_mask

# 라즈베리파이(client)에서 노트북(server)로 보내기


# def Upload(body, headers={}):
#     conn = HTTPConnection(host)
#     # body를 보낸다, 경로를 임의로 설정한다('/').노트북으로 요청이 넘어감
#     conn.request('POST', '/', body=body, headers=headers)
#     res = conn.getresponse()  # 노트북에서 요청에대한 응답을 보내는데,
#     print(res.getheaders())  # 응답 중 헤더부분만가져와서 프린드
#     # X-server2CLient 라는 key의 value를 가져오는데 없으면 fallvback을 내보내라.
#     print(res.getheader('X-Server2Client', 'Fallback'))
#     print(res.read())  # 서버가 보낸 응답의 body부분을 프린트
#     print('Uploaded to', host, 'with status', res.status)

# 이미지를 byte로 서버에 전달


# def UploadNumpy(image):
#     result, image = cv2.imencode(
#         '.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), 90])  # image 형식을 jpg로 바꾸는데 quality'90' 설정. img가 배열로 저장됨
#     if not result:
#         raise Exception('Image encode error')
#     # 이미지를 바이트로 변환 저장
#     Upload(image.tobytes(), {
#         "X-Client2Server": "123"
#     })


def set_path3(image, forward_criteria):

    height, width = image.shape
    #ratio = .1
    #end_ratio = 1 - ratio
    #print(1, image.shape)
    #image = image[
     #   int(height*ratio):,
      #  :
    #]
    #print(2, image.shape)
    #print(image)
    #height, width = image.shape
    height = height-1
    width = width-1
    center = int(width/2)
    left = 0
    right = width

    center = int((left+right)/2)

    try:
        '''if image[height][:center].min(axis=0) == 255:
            left = 0
        else:
            left = image[height][:center].argmin(axis=0)    
        if image[height][center:].max(axis=0) == 0:
            right = width
        else:    
            right = center+image[height][center:].argmax(axis=0)  
            q
        center = int((left+right)/2)'''

        print(int(first_nonzero(image[:, center], 0, height)))
        forward = min(int(height), int(
            first_nonzero(image[:, center], 0, height))-1)
        #print(height, first_nonzero(image[:,center],0,height))

        left_line = first_nonzero(
            image[height-forward:height, center:], 1, width-center)
        right_line = first_nonzero(
            np.fliplr(image[height-forward:height, :center]), 1, center)

        center_y = (np.ones(forward)*2*center-left_line+right_line)/2-center
        center_x = np.vstack((np.arange(forward), np.zeros(forward)))
        m, c = np.linalg.lstsq(center_x.T, center_y, rcond=-1)[0]  # 최소제곱법
        # result = m
        print('slope :' + str(m))
        K = 
        if image[150:160,140:180].mean() > 240:
            result = (-1, 1)
            motor(*result)
            time.sleep(1.5)
        elif abs(m) < forward_criteria:
            result = (1, 1)
            motor(*result)
        elif m > 0:
            print('left')
            P_left = 1-K*abs(m)
            result = (max(P_left, 0), 1)
            motor(*result)

        else:
            print('right')
            P_right = 1-K*abs(m)
            result = (1, max(P_right, 0))
            motor(*result)
    except:
        result = 'backward'
        m = 0

    # return result, round(m, 4), forward


def motor(left, right):
    if left > 0:
        left_f = left
        left_b = 0
    else:
        left_f = 0
        left_b = -left
    if right > 0:
        right_f = right
        right_b = 0
    else:
        right_f = 0
        right_b = -right

    p1A.ChangeDutyCycle(left_f*93)
    p1B.ChangeDutyCycle(left_b*93)
    p2A.ChangeDutyCycle(right_f*100)
    p2B.ChangeDutyCycle(right_b*100)


motor1A = 38
motor1B = 40
motor2A = 37
motor2B = 35

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(motor1A, GPIO.OUT)
GPIO.setup(motor1B, GPIO.OUT)
GPIO.setup(motor2A, GPIO.OUT)
GPIO.setup(motor2B, GPIO.OUT)

p1A = GPIO.PWM(motor1A, 1000)
p1B = GPIO.PWM(motor1B, 1000)
p2A = GPIO.PWM(motor2A, 1000)
p2B = GPIO.PWM(motor2B, 1000)

p1A.start(100)
p1B.start(100)
p2A.start(100)
p2B.start(100)


def cleanup():
    GPIO.cleanup()


atexit.register(cleanup)


def first_nonzero(arr, axis, invalid_val=-1):
    arr = np.flipud(arr)  # 사진뒤집어주는 코드
    mask = arr != 0  # 숫자가 255인 것은 True(1), 0인 것은 False(0)
    # 가로축 기준으로, 최댓값(1)의 위치를 반환, 만약 1을 발견하지 못하면 뚫려있다는 의미이므로 height 값을 반환
    return np.where(mask.any(axis=axis), mask.argmax(axis=axis), invalid_val)


def detect(img_array):
    face_cascade = cv2.CascadeClassifier('./cascade.xml')

    gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)

    objs = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in objs:
        cv2.rectangle(img_array, (x, y), (x+w, y+h), (255, 0, 0), 2)
    #cv2.imshow('img', img_array)


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

    # 이미지가 한장한장 numpy array에 저장이 된다.
    image = frame.array
    mask_image = select_white(image, 70)  # mask image array
    cv2.imshow("Processed", mask_image)
    #print(mask_image[150:160,140:180].mean())
    #cv2.imshow("Raw", image)
    # UploadNumpy(mask_image)
    detect(image)
    set_path3(mask_image, 0.08)

    key = cv2.waitKey(1) & 0xFF  # 에러 방지
    rawCapture.truncate(0)  # 에러 방지

    if key == ord('q'):
        break
