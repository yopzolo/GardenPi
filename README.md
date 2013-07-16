# GardenPi

This is an implementation of webiopi dedicated to indoor growing

* periodic switch on/off of lights, pumps.
* switch of fans based on temperature and humidity measures
* configuration of periodicity for ligths and pumps
* configuration of trigger temperature and humidity values for fans

## setup

* **get a pi ..**
* clone this repository
   * `$ git clone https://github.com/yopzolo/GardenPi.git`
* run the install script
   * `$ cd GardenPi`
   * `$ chmod +x setup.sh`
   * `$ sudo ./setup.sh`
* run webiopi as a daemon
   * `$ cd /etc/init.d`
   * `$ sudo ./webiopi start`

---

## Screenshots

![Icon](screens/Iphone_dash.png)
![Dashboard](screens/Dashboard.png)
![Config](screens/Settings.png)
![logs](screens/Logs.png)

