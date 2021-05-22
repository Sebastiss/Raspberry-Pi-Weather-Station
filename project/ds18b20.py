# THT DS18B20 read data from sensor and save it in MariaDB dataBase
import w1thermsensor
from time import sleep
import mariadb
import sys

# initialize the THT DS18B20 sensor
sensor = w1thermsensor.W1ThermSensor()

# to print degree symbol in output
degree_sign = chr(176)
# or another verion of degree symbol
# u"\N{DEGREE SIGN}"

# set the value to wait defined amount of seconds bettwen next measurements
wait = 10

# calibrate the sensor
outside_temperature = sensor.get_temperature()
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
        # read data from DS18B20 sensor
        outside_temperature = round(sensor.get_temperature(), 2)
        # insert information to data base
        try:
            # Append data to the data base
            cur.execute('''INSERT INTO ds18b20_data(outside_temperature) VALUES(%s);''', (outside_temperature,))
            # cur.execute('''INSERT INTO ds18b20_data(outside_temperature) VALUES(%s);''', (outside_temperature))
        except mariadb.Error as e:
            print(f"Error: {e}")
        
        print("{:05.2f}{}C".format(outside_temperature, degree_sign))
        # confirm the data transaction in data base
        db.commit()
        # return the ID of the last inserted row of data in data base
        print(f"Last Inserted ID: {cur.lastrowid}")
        sleep(wait)
finally:
    # Close the connection with data base
    db.close()
    print('closing connection : OK')
