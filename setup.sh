#!/bin/sh

CONFIG_FILE=/etc/webiopi/config
HOME=/usr/share/webiopi/htdocs/

SENSOR_HOME=WebIOPi-0.6.0/python/webiopi/devices/sensor
SENSOR_INIT=$SENSOR_HOME/__init__.py

echo "downloading webiopi"
wget http://webiopi.googlecode.com/files/WebIOPi-0.6.0.tar.gz
tar xvzf WebIOPi-0.6.0.tar.gz

echo "adding DHT to webiopi module"
cp DHT_X/Adafruit_DHT /usr/bin/
cp DHT_X/dht11.py $SENSOR_HOME
cp DHT_X/sensor_init.py $SENSOR_INIT

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
# sudo webiopi -c /etc/webiopi/config