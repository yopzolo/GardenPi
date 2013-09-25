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

# data codecs
#

class ConfigEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.asDict();

class ConfigFile(object):
    def __init__(self, filename):
        self.filename = filename

    def save(self, obj):
        with open(self.filename, "wb") as f:
            pickle.dump(obj, f)

    def load(self):
        with open(self.filename, "rb") as f:
            return pickle.load(f)

# state storage
#
class RegisterState(object):
    def __init__(self):
        self.time = datetime.min

        self.temp = 0.0
        self.humidity = 0.0

        self.day = False
        self.pump = False

        self.fan = False
        self.fanHigh = False
        self.brum = False
        self.brumFan = False

class RegisterStateLogger(object):
    def __init__(self, filename, period):
        self.filename = filename
        self.period = period
        self.lastLog = datetime(1970,1,1,0,0,0)

    def log(self, state):
        if state.time >= self.lastLog + self.period:
            self.lastLog = state.time
            with open(self.filename, "a") as logFile:
                logFile.write(state.time.isoformat())
                logFile.write(",")
                logFile.write(str(state.temp))
                logFile.write(",")
                logFile.write(str(state.humidity))
                logFile.write(",")
                logFile.write(str(state.day))
                logFile.write(",")
                logFile.write(str(state.pump))
                logFile.write(",")
                logFile.write(str(state.fan))
                logFile.write(",")
                logFile.write(str(state.fanHigh))
                logFile.write(",")
                logFile.write(str(state.brum))
                logFile.write("\n")
