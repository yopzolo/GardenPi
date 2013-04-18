# GardenPi

This is an implementation of webiopi dedicated to indoor growing

* periodic switch on/off of lights, pumps.
* switch of fans based on temperature and humidity measures
* configuration of periodicity for ligths and pumps
* configuration of trigger temperature and humidity values for fans

## setup

* **get a pi ..**
* download and install webiopi [instructions here](http://code.google.com/p/webiopi/wiki/INSTALL)
    * '$ wget http://webiopi.googlecode.com/files/WebIOPi-0.6.0.tar.gz'
    * '$ tar xvzf WebIOPi-0.6.0.tar.gz'
    * '$ cd WebIOPi-0.6.0'
    * '$ sudo ./setup.sh'
* clone this repository
* run webiopi from inside your clone : `$ sudo webiopi -c config`

---
