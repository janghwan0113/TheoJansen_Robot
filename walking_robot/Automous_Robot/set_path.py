import RPi.GPIO as GPIO
import cv2
import numpy as np
import time
from first_nonzero import first_nonzero
from AR_marker import AR_marker
from ultra_sonic import ultra_sonic
from detect_stop import detect_stop
from motor import motor

def set_path(image, forward_criteria, raw_image_array):

    height, width = image.shape
    height = height-1
    width = width-1
    center = int(width/2)
    left = 0
    right = width

    center = int((left+right)/2)

    try:
        forward = min(int(height), int(
            first_nonzero(image[:, center], 0, height))-1)

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
        print('slope:' + str(m), 'AR_length:'+str(AR_length), 'AR_id:'+str(AR_id),
              'Ultra_Sonic:'+str(sonic_distance), 'StopSign_length:'+str(stop_length))
        
        if image[150:160, 140:180].mean() > 240:
            result = (-1, 1)
            motor(*result)
            time.sleep(1.5)
        elif AR_id == 114 and AR_length > 35:
            motor(0, 1)
            time.sleep(1.5)
        elif AR_id == 922 and AR_length > 35:
            motor(1, 0.5)
            time.sleep(3)
        elif AR_id == 2537 and AR_length > 30:
            motor(0, 0)
            time.sleep(5)
        elif stop_length > 30:
            motor(0, 0)
            time.sleep(5)
        elif sonic_distance < 20:
            motor(0, 0)
            time.sleep(5)
        elif abs(m) < forward_criteria:
            result = (1, 1)
            motor(*result)
        elif m > 0:
            print('left')
            P = 1-K*abs(m)
            result = (max(P, 0), 1)
            motor(*result)
        elif m < 0:
            print('right')
            P = 1-K*abs(m)
            result = (1, max(P, 0))
            motor(*result)

    except Exception as error:
        print(error)