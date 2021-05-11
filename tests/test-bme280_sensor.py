#Bosh BME280 read data form sensor - test example
from smbus import SMBus
from bme280 import BME280
from time import sleep

# initialize the BME280 sensor
bus = SMBus(1) #set up the device port to 1
bme280 = BME280(i2c_dev=bus) #initialize BME sensor

#to print degree symbol in output
degree_sign = chr(176)#u"\N{DEGREE SIGN}"

#wait defined amount of seconds
wait = 10

while True:
    ambient_temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()
    print("{:05.2f}{}C {:05.2f}hPa {:05.2f}%".format(ambient_temperature, degree_sign, pressure, humidity))
    sleep(wait)
