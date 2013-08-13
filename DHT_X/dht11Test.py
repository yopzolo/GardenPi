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
    
import unittest
import re

from datetime import datetime, time, timedelta

class DHT(object):

    def __init__(self):
        self.refreshPeriod = timedelta(seconds=15)
        self.refreshing = False
        self.lastRefresh = datetime.min

        self.lastTemp = -1.0        
        self.lastHumidity = -1.0

    def filterNewValue(self, oldValue, newValue):
        if (oldValue==-1 or newValue<3*oldValue and 3*newValue>oldValue):
            return newValue
        return oldValue

    def collectData(self, output):
        if not self.refreshing:
            self.refreshing = True;

            if (len(output)>0):
                values = re.split(b";", output)

                self.lastTemp = self.filterNewValue(self.lastTemp, float(values[0]))
                self.lastHumidity = self.filterNewValue(self.lastHumidity, float(values[1]))

                self.lastRefresh = datetime.now()
            self.refreshing = False

class DHTTest(unittest.TestCase):
    def test_collectData_default(self):
        dht = DHT()
        dht.collectData("25.5;15")
        self.assertEqual(dht.lastTemp, 25.5)
        self.assertEqual(dht.lastHumidity, 15)

        dht.collectData("26;25")
        self.assertEqual(dht.lastTemp, 26)
        self.assertEqual(dht.lastHumidity, 25)

        dht.collectData("92;24")
        self.assertEqual(dht.lastTemp, 26)
        self.assertEqual(dht.lastHumidity, 24)

        dht.collectData("5;24")
        self.assertEqual(dht.lastTemp, 26)
        self.assertEqual(dht.lastHumidity, 24)