import RPi.GPIO as GPIO
import atexit

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