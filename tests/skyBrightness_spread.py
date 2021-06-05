from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
from datetime import date
from openpyxl import load_workbook  #library to work with spreadsheet

# Careate object of Picamera and set the resolution
camera = PiCamera()
camera.resolution = (640, 480)

# Load the workbook and select the sheet
wb = load_workbook('/home/pi/Documents/brightness.xlsx')
sheet = wb['Arkusz1']

try:
  while True:
    today = date.today().strftime("%d/%m/%Y")
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

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

    # Inform the user!
    print("Addin data to the spreadsheet: ")
    print("{} {} {}".format(today, current_time, avg))
	
		# Append data to the spreadsheet
    row = (today, current_time, avg)
    sheet.append(row)
		
		#Save the workbook
    wb.save('/home/pi/Documents/brightness.xlsx')
    
		# Wait for 10 minutes seconds (600 seconds)
    time.sleep(600)
    # time.sleep(10)
finally:
	# Make sure the workbook is saved!
	wb.save('/home/pi/Documents/brightness.xlsx')
  
	print('Saveing process finished successfully. Goodbye!')
