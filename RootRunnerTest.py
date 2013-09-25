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

from DayRunner import DayConfig, DayRunner
from config import RegisterState,RegisterStateLogger
from RootConfig import RootConfig, RootRunner

from RunnerMock import RunnerMock

class RootRunnerTest(unittest.TestCase):

    def test_run_active_config(self):
        config = RootConfig();
        config.configs = [DayConfig(), DayConfig(), DayConfig()]
        config.activeConfig = config.configs[1]

        current = RegisterState()
        current.time = datetime.now()

        runner = RootRunner()
        runner.runner = RunnerMock()

        runner.update(config, current)
        
        self.assertEqual(runner.runner.config, config.configs[1])
        self.assertEqual(runner.runner.state, current)
