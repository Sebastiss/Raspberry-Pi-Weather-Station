#!/bin/bash


cd $HOME/Documents/weather_station

python3 bme280sensor.py
python3 camera.py &
python3 ds18b20.py

exit 0