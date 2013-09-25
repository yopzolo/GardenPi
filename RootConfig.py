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

from DayRunner import DayRunner, DayConfig
#
# data updater
#
class RootRunner(object):
    def __init__(self):
        self.runner = DayRunner()

    def updateTime(self, config, state):
        state.time = datetime.now()
        self.update(config, state)

    def update(self, config, state):
        self.runner.update(config.activeConfig, state)


class RootConfig(object):
    def __init__(self):
        self.configs = [DayConfig()]
        self.activeConfig = self.configs[0]
    
    def asDict(self):
        return self.activeConfig.asDict()
