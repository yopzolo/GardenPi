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

from UrneRunner import UrneConfig, UrneRunner

class DayRunner(object):
    def __init__(self):
        self.runner = UrneRunner()

    def update(self, config, state):
        if config.di.startTime > config.noct.startTime:
            state.day = state.time.time() > config.di.startTime or state.time.time() < config.noct.startTime
        else:
            state.day = state.time.time() > config.di.startTime and state.time.time() < config.noct.startTime

        currentConfig = config.di if state.day else config.noct

        self.runner.update(currentConfig, state)


class DayConfig(object):
    def __init__(self):
        self.di = UrneConfig();
        self.noct = UrneConfig();

    def asDict(self):
        return {'day':self.di.asDict(),'night':self.noct.asDict()}
