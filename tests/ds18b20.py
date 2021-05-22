import w1thermsensor
from time import sleep
 
sensor = w1thermsensor.W1ThermSensor()
while True: 
	temp = round(sensor.get_temperature(), 2)
	print(temp)
	sleep(3)
