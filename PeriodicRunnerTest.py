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
import json
import string
import os
from datetime import datetime, time, timedelta

from config import RegisterState,RegisterStateLogger
from config import ConfigEncoder, ConfigFile

from DayRunner import DayConfig, DayRunner
from UrneRunner import UrneConfig, UrneRunner
from PeriodicRunner import PeriodicConfig, PeriodicRunner
from TriggerRunner import TriggerConfig, TriggerRunner
from DelayRunner import DelayRunner
from RunnerMock import RunnerMock
from ConfigDictMock import ConfigDictMock

class PeriodicRunnerTest(unittest.TestCase):
    def test_period(self):
        config = PeriodicConfig()

        config.period = timedelta(minutes = 3)
        config.duration = timedelta(minutes = 1)

        runner = PeriodicRunner()
        for minNb in range(0, 59):
            self.assertEqual(runner.valueAtTime(config, datetime(1981,11,2,17,minNb,0)), minNb%3==0)

    def test_period_skipUpdates(self):
        config = PeriodicConfig()
        config.period = timedelta(minutes = 5)
        config.duration = timedelta(minutes = 2)

        expected = [True, True, False, False, False, True, True, False, False, False, True, True, False, False, False, True, True]

        runner = PeriodicRunner()
        self.assertEqual(runner.valueAtTime(config, datetime(1981,11,2,17,0,0)), expected[0])
        self.assertEqual(runner.valueAtTime(config, datetime(1981,11,2,17,5,0)), expected[5])
        self.assertEqual(runner.valueAtTime(config, datetime(1981,11,2,17,11,0)), expected[11])

class PeriodicConfigTest(unittest.TestCase):
    def test_dump(self):
        config = PeriodicConfig()
        config.period = timedelta(minutes = 5)
        config.duration = timedelta(minutes = 2)

        self.assertEqual(json.dumps(config.asDict()), "{\"duration\": 120.0, \"period\": 300.0}")
        # print json.dumps(config, cls=ConfigEncoder, indent=4)
        