#!/usr/bin/python3

"""
Bosch BME280
====================================
Read indoor measurements.
The BME280 can measure temperature, humidity and preasurein the same periods of time.
The indoot meteo data are displayed on the screen and saved in MariaDB Data Base 
"""

#Bosh BME280 read data form sensor
from smbus import SMBus
from bme280 import BME280
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

def readData(sensor, cur, db, wait):
    """
    Read data from BME280 sensor
    :param sensor: object describring the sensor
    :param cur: cursor of the database
    :param db: db object
    :param wait (int): value which defined amount of seconds bettwen next measurements
    """
    degree_sign = chr(176)
    # read data from BME280 sensor
    ambient_temperature = round(sensor.get_temperature(), 2)
    pressure = round(sensor.get_pressure(), 2)
    humidity = round(sensor.get_humidity(), 2)
    # insert information to data base
    try:
        # Append data to the data base
        cur.execute("INSERT INTO bme280_data(ambient_temperature, pressure, humidity) VALUES (%s, %s, %s)", 
            (ambient_temperature, pressure, humidity))
    except mariadb.Error as e:
        print(f"Error: {e}")
    
    print("{:05.2f}{}C {:05.2f}hPa {:05.2f}%".format(ambient_temperature, degree_sign, pressure, humidity))
    # confirm the data transaction in data base
    db.commit()
    # return the ID of the last inserted row of data in data base
    print(f"Last Inserted ID: {cur.lastrowid}")
    sleep(wait)

def calibrateSensor(sensor):
    """
    Calibrate the sensor by make firs measurements by the sensor which won't be save in database
    :param sensor: object of initialized sensor
    """
    temperature = sensor.get_temperature()
    pressure = sensor.get_pressure()
    humidity = sensor.get_humidity()
    sleep(3)


def readInsideData():
    """
    Main loop of the **bme280sensor** scipt
    """

    # initialize the BME280 sensor
    port = 1
    bus = SMBus(port) # set up the device on port number 1
    sensor = BME280(i2c_dev=bus) # initialize BME sensor

    # calibrate the sensor
    calibrateSensor(sensor)

    cur, db = connect()

    try:
        while True:
            readData(sensor, cur, db, 10)
    finally:
        # Close the connection with data base
        db.close()
        print('closing connection : OK')

if __name__ == '__main__':
    readInsideData()