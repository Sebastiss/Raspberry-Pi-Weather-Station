import w1thermsensor
from time import sleep

 #initialize the sensor
sensor = w1thermsensor.W1ThermSensor()

# to print degree symbol in output
degree_sign = chr(176)
# or another verion of degree symbol
# u"\N{DEGREE SIGN}"

while True: 
	temp = round(sensor.get_temperature(), 2)
	print('{:05.2f}{}C'.format(temp, degree_sign))
	sleep(3)
