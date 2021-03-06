#   Copyright 2012-2013 Eric Ptak - trouch.com
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import webiopi
from webiopi.protocols.rest import *

class Humidity():
    def __family__(self):
        return "Humidity"
    
    def __getHumidity__(self):
        raise NotImplementedError

    @request("GET", "sensor/humidity")
    @response("%.02f")
    def getHumidity(self):
        return self.__getHumidity__()
 

import subprocess
import re

from webiopi.devices.sensor import Temperature
from datetime import datetime, time, timedelta

class DHT(Humidity, Temperature):
    def __family__(self):
        return "Humidity-Temperature"

    def __init__(self, gpio=0x00, name="DHT11"):
        self.gpioPort = gpio;

        self.refreshPeriod = timedelta(seconds=15)
        self.refreshing = False
        self.lastRefresh = datetime.min

        self.lastTemp = -1.0        
        self.lastHumidity = -1.0

        self.collectData()

    def filterNewValue(self, oldValue, newValue):
        if (oldValue==-1 or newValue<3*oldValue and 3*newValue>oldValue):
            return newValue
        return oldValue

    def collectData(self):
        webiopi.debug('Adafruit_DHT collecting fresh Data')
        if not self.refreshing:
            self.refreshing = True;

            output = subprocess.check_output(["Adafruit_DHT", self.__type__(), self.gpioPort]);
            if (len(output)>0):
                values = re.split(b";", output)

                self.lastTemp = self.filterNewValue(self.lastTemp, float(values[0]))
                self.lastHumidity = self.filterNewValue(self.lastHumidity, float(values[1]))

                self.lastRefresh = datetime.now()
            self.refreshing = False

    def __getKelvin__(self):
        return self.Celsius2Kelvin()

    def __getCelsius__(self):
        if datetime.now() >= self.lastRefresh + self.refreshPeriod:
            self.collectData()

        return self.lastTemp

    def __getFahrenheit__(self):
        return self.Celsius2Fahrenheit()

    def __getHumidity__(self):
        if datetime.now() >= self.lastRefresh + self.refreshPeriod:
            self.collectData()

        return self.lastHumidity

    def close(self):
        return 0

class DHT11(DHT):

    def __type__(self):
        return "11"

class DHT2302(DHT):

    def __type__(self):
        return "2302"
