#!/usr/bin/python3

"""
camera
================================================================================
Read brightness value form camera module in the same periods of time.
The brightness data are displayed on the screen and saved in MariaDB Data Base 
"""

from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
from time import sleep
import mariadb
import sys

def connect():
    """
    Initialize the connection with MariaDB Server and insert data in selected table
    :return cur: cursor of the database
    :return db: object of the opened database
    """
    try:
        db = mariadb.connect(host='localhost',
                                user='admin',
                                passwd='admin',
                                db='weather_station')
        print('Connect to data base : OK')
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    cur = db.cursor()
    return cur, db


def readData(camera, cur, db, wait):
    """
    Set up the camera and take a picture
    Read data from each pixel and get vaule
    Next convert the picture color model from BGR to HSV 
    Calculating the average vaule from picture
    insert information to data base
    :param sensor: object describring the sensor
    :param cur: cursor of the database
    :param db: db object
    :param wait (int): value which defined amount of seconds bettwen next measurements
    """
    imageCapture = PiRGBArray(camera, size = (640,480))
    camera.capture(imageCapture, format="bgr")
    image = imageCapture.array
    # Converting the picture from BGR to HSV model color 
    imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    s = 0
    it = 0
    # calculating the average vaule from picture
    # read data from each pixel and get vaule
    for row in imageHSV:
      for col in row:
        s = s + col[2] # value
        it = it + 1
    # Value range is [0,255]
    # averge of vaule from HSV Color model
    avg = s/it
    # percent average
    percentavg = round((avg*100)/255,2)

    print(round(avg, 2))

    # seting up down vaule for each section
    # sunny down value
    sunny = 171
    # cloudy down value
    cloudy = 143
    # overcast down value
    overcast = 98
    # night down value
    night = 0

    # insert information to data base
    try:
      # Append data to the data base
      # section - for my purpose I defined four individual groups
      if avg >= night and avg < overcast:
          cur.execute('''INSERT INTO camera_data(value, description, percentage_intensity) VALUES(%s,%s,%s);''', (avg, "NIGHT", percentavg))
          print("NIGHT ", round(avg, 2), percentavg)
      if avg >= overcast and avg < cloudy:
          cur.execute('''INSERT INTO camera_data(value, description, percentage_intensity) VALUES(%s,%s,%s);''', (avg, "OVERCAST", percentavg))
          print("OVERCAST ", round(avg, 2), percentavg)
      if avg >= cloudy and avg < sunny:
          cur.execute('''INSERT INTO camera_data(value, description, percentage_intensity) VALUES(%s,%s,%s);''', (avg, "CLOUDY", percentavg))
          print("CLOUDY ", round(avg, 2), percentavg)
      if avg >= sunny and avg <= 255:
          cur.execute('''INSERT INTO camera_data(value, description, percentage_intensity) VALUES(%s,%s,%s);''', (avg, "SUNNY", percentavg))
          print("SUNNY ", round(avg, 2), percentavg)
    except mariadb.Error as e:
        print(f"Error: {e}")
        
    # confirm the data transaction in data base
    db.commit()
    # return the ID of the last inserted row of data in data base
    print(f"Last Inserted ID: {cur.lastrowid}")

    # Wait defined amount of time (in secounds)
    sleep(wait)


def readBrightness():
    """
    Main loop of the **camera** scipt
    """
    # Careate object of Picamera and set the resolution
    camera = PiCamera()
    camera.resolution = (640, 480)

    # set the value to wait defined amount of seconds bettwen next measurements

    cur, db = connect()

    try:
        while True:
            readData(camera, cur, db, 10)
    finally:
        # Close the connection with data base
        db.close()
        print('closing connection : OK')

if __name__ == '__main__':
    readBrightness()