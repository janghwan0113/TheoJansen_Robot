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
from ar_markers import detect_markers
from glob import glob
# 수동제어 관련 라이브러리
import json
from time import sleep
from Time import Time
from sys import argv
import os

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


def set_path3(image, forward_criteria, raw_image_array):

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

        #print(int(first_nonzero(image[:, center], 0, height)))
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
        K = 2.8
        AR_length, AR_id = AR_marker(raw_image_array)
        sonic_distance = ultra_sonic()
        stop_length = detect_stop(raw_image_array)
        print('slope:' + str(m),'AR_length:'+str(AR_length),'AR_id:'+str(AR_id), 'Ultra_Sonic:'+str(sonic_distance),'StopSign_length:'+str(stop_length))
 
        if image[150:160,140:180].mean() > 240:
            result = (-1, 1)
            motor(*result)
            time.sleep(1.2)
        elif AR_id == 114 and AR_length > 35:
            motor(0.5, 1)
            time.sleep(3)
        elif AR_id == 922 and AR_length > 35:
            motor(1, 0.5)
            time.sleep(3)
        elif AR_id == 2537 and AR_length > 30:
            motor(0, 0)
            time.sleep(5)
        elif sonic_distance < 20:
            motor(0, 0)
            time.sleep(5)
        elif abs(m) < forward_criteria:
            result = (1, 1)
            motor(*result)
        else:
            print('else')
            P = 1-K*abs(m)
            result =  (max(P, 0), 1) if m > 0 else (1, max(P, 0))
            motor(*result)
    except Exception as error:
        print(error)

    # return result, round(m, 4), forward

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

def cleanup():
    GPIO.cleanup()


atexit.register(cleanup)

def first_nonzero(arr, axis, invalid_val=-1):
    arr = np.flipud(arr)  # 사진뒤집어주는 코드
    mask = arr != 0  # 숫자가 255인 것은 True(1), 0인 것은 False(0)
    # 가로축 기준으로, 최댓값(1)의 위치를 반환, 만약 1을 발견하지 못하면 뚫려있다는 의미이므로 height 값을 반환
    return np.where(mask.any(axis=axis), mask.argmax(axis=axis), invalid_val)

def detect_stop(img_array):
    face_cascade = cv2.CascadeClassifier('./cascade.xml')

    gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)

    objs = face_cascade.detectMultiScale(gray, 1.3, 5)
    if (len(objs)):
        length = objs[0][3]
        for (x, y, w, h) in objs:
            cv2.rectangle(img_array, (x, y), (x+w, y+h), (255, 0, 0), 2)
    else :
        length = 0       
    cv2.imshow('img', img_array)
    return length

def AR_marker(img_array):
    markers = detect_markers(img_array)   #배열을 리턴
    length, id_num = (0,0)
    for marker in markers :
        crdt_x, crdt_y = ([], [])
        for i in range(4):
            crdt_x.append(marker.contours[i][0][0])
            crdt_y.append(marker.contours[i][0][1]) 
        marker.highlite_marker(img_array)
        length = max(crdt_x)-min(crdt_x)
        id_num = marker.id
    print(length, id_num)
    cv2.imshow('img', img_array)
    return length, id_num 



GPIO_TRIGGER = 10
GPIO_ECHO    = 12
 
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.output(GPIO_TRIGGER, False)

def ultra_sonic():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()
    timeOut = start

    while GPIO.input(GPIO_ECHO)==0:
        start = time.time()
        if time.time()-timeOut > 0.05:
            return -1

    while GPIO.input(GPIO_ECHO)==1:
        if time.time()-start > 0.05:
            return -1
        stop = time.time()

    elapsed = stop-start
    distance = (elapsed * 34300)/2
    return distance

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
    mask_image = select_white(image, 150)  # mask image array

    #print(mask_image[150:160,140:180].mean())
    #UploadNumpy(mask_image)
    #detect_stop(image)
    #set_path3(mask_image, 0.04, image)
    AR_marker(image)
    #ultra_sonic()
    #cv2.imshow("Processed", mask_image)
    #cv2.imshow("Raw", image)

    key = cv2.waitKey(1) & 0xFF  # 에러 방지
    rawCapture.truncate(0)  # 에러 방지

    if key == ord('q'):
        break



'''
class AR_test:
  def __iter__(self):
    self.streaming_obj = iter(sorted(glob('streaming/*.jpg',recursive=True)))
    return self

  def __next__(self):
    path = next(self.streaming_obj)
    print(path)
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    return img

for img in AR_test():
    AR_marker(img)
    #cv2.imshow("Raw", img)
    key = cv2.waitKey(200) & 0xFF  # 에러 방지
    
    
    # 바이트를 array로 만들고
    data = np.asarray(bytearray(data), dtype="uint8")
    img = cv2.imdecode(data, cv2.IMREAD_ANYCOLOR)  # 이미지 형식을 바꿔주고
    # AR_Marker
    markers = detect_markers(img)   #배열을 리턴
    for marker in markers :
        print('detected',marker,id)
        marker.highlite_marker(img)
    cv2.imshow('image', img)  # 이미지를 보여준다
    cv2.waitKey(1)
'''