#!/bin/bash

cd $HOME
sudo apt-get update
sudo apt-get upgrade -y

# Open CV
sudo apt install python3-pip
sudo apt install libatlas-base-dev -y
sudo apt install libjasper-dev -y
sudo apt install libqtgui4 -y
sudo apt install python3-pyqt5 -y
sudo apt install libqt4-test -y
sudo apt install libhdf5-dev libhdf5-serial-dev -y
sudo pip3 install opencv-contrib-python==4.1.0.25
pip3 install picamera[array]

# Bosh BME280
mkdir $HOME/Documents/weather_station
sudo pip3 install pimoroni-bme280 smbus
