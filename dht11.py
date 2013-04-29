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

class DHT11(Humidity, Temperature):

    gpioPort = 0
    temperature = 25.0
    humidity = 24.0

    def __family__(self):
        return "Humidity-Temperature"

    def __init__(self, gpio=0x00, name="DHT11"):
        gpioPort = gpio;
        
    def refreshValues(self):
        output = subprocess.check_output(["./Adafruit_DHT", "11", "4"]);
        matches = re.search("Temp =\s+([0-9.]+)", output)
        global temperature
        temperature = float(matches.group(1))
        global humidity
        matches = re.search("Hum =\s+([0-9.]+)", output)
        humidity = float(matches.group(1))

    def __getKelvin__(self):
        return self.Celsius2Kelvin()

    def __getCelsius__(self):
        return 25.0
    
    def __getFahrenheit__(self):
        return self.Celsius2Fahrenheit()


    def __getHumidity__(self):
        return 23.0

    def close(self):
        return 0
