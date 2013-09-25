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

class DelayRunnerTest(unittest.TestCase):
    def test_delay(self):
        runner = DelayRunner(timedelta(minutes = 1));

        self.assertEqual(runner.valueWithValueAtTime(False, datetime(1981,11,2,17,0,0)), False)
        self.assertEqual(runner.valueWithValueAtTime(False, datetime(1981,11,2,17,1,0)), False)
        self.assertEqual(runner.valueWithValueAtTime(True, datetime(1981,11,2,17,1,30)), False)
        self.assertEqual(runner.valueWithValueAtTime(True, datetime(1981,11,2,17,02,01)), False)
        self.assertEqual(runner.valueWithValueAtTime(True, datetime(1981,11,2,17,03,00)), True)
        self.assertEqual(runner.valueWithValueAtTime(False, datetime(1981,11,2,17,04,01)), True)
        self.assertEqual(runner.valueWithValueAtTime(False, datetime(1981,11,2,17,05,02)), False)
      