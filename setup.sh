#!/bin/sh

#     Copyright 2013 paul blin

# This file is part of GardenPi.

#     GardenPi is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     GardenPi is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with GardenPi.  If not, see <http://www.gnu.org/licenses/>.
    
CONFIG_FILE=/etc/webiopi/config
HOME=/usr/share/webiopi/htdocs/

SENSOR_HOME=WebIOPi-0.6.0/python/webiopi/devices/sensor
SENSOR_INIT=$SENSOR_HOME/__init__.py

echo "Downloading webiopi"
wget http://webiopi.googlecode.com/files/WebIOPi-0.6.0.tar.gz
tar xvzf WebIOPi-0.6.0.tar.gz

echo "Adding DHT to webiopi module"
cp DHT_X/Adafruit_DHT /usr/bin/
cp DHT_X/dht11.py $SENSOR_HOME
cp DHT_X/sensor_init.py $SENSOR_INIT

echo "Removing previous build if exists"
rm -r WebIOPi-0.6.0/python/build
rm -r WebIOPi-0.6.0/python/dist

echo "Removing old g4rdenP1 configuration"
rm $HOME/GardenPyConfig.pyc

echo "Installing webiopi"
cd WebIOPi-0.6.0
./setup.sh
cd ..

echo "Copying g4rdenP1 configuration"
cp config $CONFIG_FILE

cp DHT_X/dht11.js $HOME
cp htdocs/* $HOME

cp garden.py $HOME
cp config.py $HOME

/./etc/init.d/webiopi restart