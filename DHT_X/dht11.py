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

webiopi.setDebug()

class DHT(Humidity, Temperature):

    gpioPort = 0

    def __family__(self):
        return "Humidity-Temperature"

    def __init__(self, gpio=0x00, name="DHT11"):
        gpioPort = gpio;

    def __getKelvin__(self):
        return self.Celsius2Kelvin()

    def __getCelsius__(self):
        output = subprocess.check_output(["Adafruit_DHT", self.__type__(), "4"]);
        if (len(output)>0):
            return float(re.split(b";", output)[0])
        else:
            return 0.0

    def __getFahrenheit__(self):
        return self.Celsius2Fahrenheit()


    def __getHumidity__(self):
        output = subprocess.check_output(["Adafruit_DHT", self.__type__(), "4"]);
        if (len(output)>0):
            return float(re.split(b";", output)[1])
        else:
            return 0.0

    def close(self):
        return 0

class DHT11(DHT):

    def __type__(self):
        return "11"

class DHT2302(DHT):

    def __type__(self):
        return "2302"
