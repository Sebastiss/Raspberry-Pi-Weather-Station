#!/usr/bin/python3

"""
ds18b20
====================================
Read outside temperature from the DS18B20 sensor and save it in MariaDB Data Base
Read outside temperature using weatherproof probe containing DS18B20 sensor. 
This script get data from the sensor and save them in the same periods of time.
"""


import w1thermsensor
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
    Read data from DS18B20 sensor
    :param sensor: object describring the sensor
    :param cur: cursor of the database
    :param db: db object
    :param wait (int): value which defined amount of seconds bettwen next measurements
    """
    degree_sign = chr(176)
    outside_temperature = round(sensor.get_temperature(), 2)
    # insert information to data base
    try:
        # Append data to the data base
        cur.execute('''INSERT INTO ds18b20_data(outside_temperature) VALUES(%s);''', (outside_temperature,))
    except mariadb.Error as e:
        print(f"Error: {e}")

    print("{:05.2f}{}C".format(outside_temperature, degree_sign))
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
    outside_temperature = sensor.get_temperature()
    sleep(3)


def readOutsideTemp():
    """
    Main loop of the **ds18b20** scipt
    """
    # initialize the DS18B20 sensor
    sensor = w1thermsensor.W1ThermSensor()

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
    readOutsideTemp()
