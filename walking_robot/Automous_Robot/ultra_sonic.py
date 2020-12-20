import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO_TRIGGER = 10
GPIO_ECHO = 12

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.output(GPIO_TRIGGER, False)


def ultra_sonic():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()
    timeOut = start

    while GPIO.input(GPIO_ECHO) == 0:
        start = time.time()
        if time.time()-timeOut > 0.05:
            return -1

    while GPIO.input(GPIO_ECHO) == 1:
        if time.time()-start > 0.05:
            return -1
        stop = time.time()

    elapsed = stop-start
    distance = (elapsed * 34300)/2
    return distance