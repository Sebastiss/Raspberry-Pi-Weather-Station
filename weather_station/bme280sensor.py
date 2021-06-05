#Bosh BME280 read data form sensor - test example
from smbus import SMBus
from bme280 import BME280
from time import sleep
import mariadb
import sys

# initialize the BME280 sensor
port = 1
bus = SMBus(port) # set up the device on port number 1
bme280 = BME280(i2c_dev=bus) # initialize BME sensor

# to print degree symbol in output
degree_sign = chr(176)
# or another verion of degree symbol
# u"\N{DEGREE SIGN}"

# set the value to wait defined amount of seconds bettwen next measurements
wait = 10

# calibrate the sensor
temperature = bme280.get_temperature()
pressure = bme280.get_pressure()
humidity = bme280.get_humidity()
sleep(3)

# initialize the connection with MariaDB Server
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

try:
    while True:
        # read data from BME280 sensor
        ambient_temperature = round(bme280.get_temperature(), 2)
        pressure = round(bme280.get_pressure(), 2)
        humidity = round(bme280.get_humidity(), 2)
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
finally:
    # Close the connection with data base
    db.close()
    print('closing connection : OK')
