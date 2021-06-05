try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280
from time import sleep

port = 1
# initialize the sensor
bus = SMBus(port)
bme280 = BME280(i2c_dev=bus)

# to print degree symbol in output
degree_sign = chr(176)
# or another verion of degree symbol
# u"\N{DEGREE SIGN}"

# set time in seconds bettwen measurements
wait = 10

# calibrate the sensor
temperature = bme280.get_temperature()
pressure = bme280.get_pressure()
humidity = bme280.get_humidity()
sleep(3)

while True:
    temperature = round(bme280.get_temperature(), 2)
    pressure = round(bme280.get_pressure(), 2)
    humidity = round(bme280.get_humidity(), 2)
    print("{:05.2f}{}C {:05.2f}hPa {:05.2f}%".format(temperature, degree_sign, pressure, humidity))
    sleep(wait)
