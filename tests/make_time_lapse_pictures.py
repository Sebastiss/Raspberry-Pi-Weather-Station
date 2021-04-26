from time import sleep
from picamera import PiCamera

WAIT_TIME = 10 #time between pictures in secounds

camera = PiCamera()
camera.resolution = (1024, 768) #set the resolution of camera pictures

while(True):
    try:
        camera.start_preview()
        sleep(10)
        camera.capture('/home/pi/Documents/time-lapse/img{timestamp:%H-%M-%S-%f}.jpg')
        #camera.capture_continuous('/home/pi/Documents/time-lapse/img{timestamp:%D-%M-%Y-%H-%M-%S-%f}.jpg')
        camera.stop_preview()
        #sleep(WAIT_TIME)
    except KeyboardInterrupt: #make pictures untill any key is pressed
        break


