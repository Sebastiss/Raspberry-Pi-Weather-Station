from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time


camera = PiCamera()
camera.resolution = (640, 480)

while True:
  imageCapture = PiRGBArray(camera, size = (640,480))
  camera.capture(imageCapture, format="bgr")
  image = imageCapture.array
  imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  s = 0
  it = 0
  for row in imageHSV:
    for col in row:
      s = s + col[2] # value
      it = it + 1
  # Value range is [0,255]
  avg = s/it
  t1 = 75
  t2 = 160
  print(avg)
  if avg >= 0 and avg <= t1:
    print("NIGHT")
  if avg > t1 and avg <= t2:
      print("CLOUDY")
  if avg > t2 and avg <= 255:
      print("SUNNY")
  time.sleep(10)
# cv2.waitKey(0)
