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

class TriggerRunner(object):
    def __init__(self):
        self.previousValue = False
        self.isterezis = 0.5

    def valueWithValue(self, triggerConfig, value):
        if self.previousValue:
            result = value>triggerConfig.triggerValue-self.isterezis
        else:
            result = value>=triggerConfig.triggerValue+self.isterezis
        self.previousValue = result

        return result if triggerConfig.mode else not result

class TriggerConfig(object):
    def __init__(self):
        self.mode = True # True = Sup
        self.triggerValue = 0.0

    def asDict(self):
        return {'mode':self.mode,'value':self.triggerValue}
