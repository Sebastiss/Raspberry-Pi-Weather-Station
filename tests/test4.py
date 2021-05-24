from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
from time import sleep

# Careate object of Picamera and set the resolution
camera = PiCamera()
camera.resolution = (640, 480)

# set the value to wait defined amount of seconds bettwen next measurements
wait = 10

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
  # averge of vaule from HSV Color model
  avg = s/it

  print(avg)

  # sunny down value
  sunny = 171
  # cloudy down value
  cloudy = 143
  # overcast down value
  overcast = 98
  # night down value
  night = 0

  if avg >= night and avg < overcast:
    print("NIGHT ", round(avg, 2))
  if avg >= overcast and avg < cloudy:
      print("OVERCAST ", round(avg, 2))
  if avg >= cloudy and avg < sunny:
      print("CLOUDY ", round(avg, 2))
  if avg >= sunny and avg <= 255:
      print("SUNNY ", round(avg, 2))

  sleep(wait)
