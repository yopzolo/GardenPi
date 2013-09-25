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

class TriggerRunnerTest(unittest.TestCase):
    def test_triggerSup(self):
        config = TriggerConfig()
        config.mode = True # value > trigger
        config.triggerValue = 15.0

        runner = TriggerRunner()
        runner.isterezis = 1
        self.assertEqual(runner.valueWithValue(config, 12.0), False)
        self.assertEqual(runner.valueWithValue(config, 13.0), False)
        self.assertEqual(runner.valueWithValue(config, 14.0), False)
        self.assertEqual(runner.valueWithValue(config, 15.0), False)
        self.assertEqual(runner.valueWithValue(config, 16.0), True)
        self.assertEqual(runner.valueWithValue(config, 15.5), True)
        self.assertEqual(runner.valueWithValue(config, 15.0), True)
        self.assertEqual(runner.valueWithValue(config, 15.0), True)
        self.assertEqual(runner.valueWithValue(config, 14.0), False)
        self.assertEqual(runner.valueWithValue(config, 14.0), False)
        self.assertEqual(runner.valueWithValue(config, 15.5), False)
        
    def test_triggerInf(self):
        config = TriggerConfig()
        config.mode = False # value < trigger
        config.triggerValue = 45.0

        runner = TriggerRunner()
        runner.isterezis = 1
        self.assertEqual(runner.valueWithValue(config, 40.0), True)
        self.assertEqual(runner.valueWithValue(config, 44.0), True)
        self.assertEqual(runner.valueWithValue(config, 45.0), True)
        self.assertEqual(runner.valueWithValue(config, 46.0), False)
        self.assertEqual(runner.valueWithValue(config, 45.0), False)
        self.assertEqual(runner.valueWithValue(config, 44.5), False)
        self.assertEqual(runner.valueWithValue(config, 44.0), True)
        self.assertEqual(runner.valueWithValue(config, 44.5), True)
        self.assertEqual(runner.valueWithValue(config, 45.0), True)
        self.assertEqual(runner.valueWithValue(config, 45.5), True)
        self.assertEqual(runner.valueWithValue(config, 46.5), False)


class TriggerConfigTest(unittest.TestCase):
    def test_dump(self):
        config = TriggerConfig()
        config.mode = True;
        config.triggerValue = 25.0

        self.assertEqual(json.dumps(config.asDict()), "{\"mode\": true, \"value\": 25.0}")
