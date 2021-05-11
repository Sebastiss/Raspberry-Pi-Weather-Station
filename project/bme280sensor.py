try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280
from time import sleep

port = 1
#initialize the sensor
bus = SMBus(port)
bme280 = BME280(i2c_dev=bus)

# set time in seconds bettwen measurements
wait = 10

# calibrate the sensor
temperature = bme280.get_temperature()
pressure = bme280.get_pressure()
humidity = bme280.get_humidity()
sleep(3)

while True:
    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()
    print(temperature, pressure, humidity)
    sleep(wait)
