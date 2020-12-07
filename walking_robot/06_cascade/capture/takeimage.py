from picamera import PiCamera
from time import sleep

camera = PiCamera()


camera.start_preview()
camera.vflip = True
camera.hflip = True
for i in range(100):
    sleep(0.2)
    camera.capture(
        '/home/pi/walking_robot/06_cascade/capture/positive/image%s.jpg' % i)

    camera.stop_preview()
