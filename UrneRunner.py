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

from PeriodicRunner import PeriodicConfig, PeriodicRunner
from TriggerRunner import TriggerConfig, TriggerRunner
from DelayRunner import DelayRunner

class UrneRunner(object):
    def __init__(self):
        self.pumpRunner = PeriodicRunner()
        self.fanRunner = TriggerRunner()
        self.fanHighRunner = TriggerRunner()
        self.brumRunner = TriggerRunner()
        self.brumFanRunner = DelayRunner(timedelta(seconds = 30))

    def update(self, config, state):
        state.pump = self.pumpRunner.valueAtTime(config.pumpPeriod, state.time)
        state.fan = self.fanRunner.valueWithValue(config.fanTrigger, state.temp)
        state.fanHigh = self.fanHighRunner.valueWithValue(config.fanHighTrigger, state.temp)
        state.brum = self.brumRunner.valueWithValue(config.brumTrigger, state.humidity)
        state.brumFan = self.brumFanRunner.valueWithValueAtTime(state.brum, state.time)

class UrneConfig(object):
    def __init__(self):
        self.startTime = time.min
        self.pumpPeriod = PeriodicConfig()
        self.fanTrigger = TriggerConfig()
        self.fanHighTrigger = TriggerConfig()
        self.brumTrigger = TriggerConfig()

    def asDict(self):
        return {'start':self.startTime.isoformat(),'pump':self.pumpPeriod.asDict(), 'fan':self.fanTrigger.asDict(), 'fan_high':self.fanHighTrigger.asDict(), 'brum':self.brumTrigger.asDict()}
