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
    
from datetime import datetime, time, timedelta
import json
import pickle

class DelayRunner(object):
    def __init__(self, delay):
        self.delay = delay
        self.lastValue = False
        self.lastChange = datetime(1970,1,1,0,0,0)

    def valueWithValueAtTime(self, value, time):
        if self.lastValue != value:
            self.lastChange = time    
            self.lastValue = value

        if time > self.lastChange + self.delay:
            return value

        return not value
