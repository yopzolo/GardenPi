#!/bin/sh

CONFIG_FILE=/etc/webiopi/config
HOME=/usr/share/webiopi/htdocs/

SENSOR_HOME=WebIOPi-0.6.0/python/webiopi/devices/sensor
SENSOR_INIT=$SENSOR_HOME/__init__.py

echo "downloading webiopi"
wget http://webiopi.googlecode.com/files/WebIOPi-0.6.0.tar.gz
tar xvzf WebIOPi-0.6.0.tar.gz

echo "adding DHT11 to webiopi module"
cp Adafruit_DHT $SENSOR_HOME
cp dht11.py $SENSOR_HOME
cp sensor_init.py $SENSOR_INIT

echo "installing webiopi"
cd WebIOPi-0.6.0
./setup.sh
cd ..

echo "copying g4rdenP1 configuration"
cp config $CONFIG_FILE
cp config.html $HOME
cp index.html $HOME
cp light.py $HOME

/./etc/init.d/webiopi restart
