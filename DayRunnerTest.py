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
from datetime import datetime, time, timedelta

from config import RegisterState,RegisterStateLogger
from DayRunner import DayConfig, DayRunner

from RunnerMock import RunnerMock
from ConfigDictMock import ConfigDictMock

class DayRunnerTest(unittest.TestCase):
    def setUp(self):
        self.config = DayConfig()
        self.runner = DayRunner()
        self.runner.runner = RunnerMock()
        self.current = RegisterState()

    def assertConfig(self, date, expectedDay):
        self.current.time = date
        self.runner.update(self.config, self.current)

        # print '- {} {}'.format(date, "Day" if self.current.day else "Nigth")

        self.assertIs(self.runner.runner.config, self.config.di if expectedDay else self.config.noct)
        self.assertEqual(self.runner.runner.state, self.current)
        self.assertEqual(self.current.day, expectedDay)        
 
    def runTest(self,expectedResult):
        for day in range(1,10):
            for hour in range(0,24):
                self.assertConfig(datetime(2018,7,day,hour,0,1), expectedResult[hour])

    def test_dayConfigNightIsDay(self):
        self.config.di.startTime = time(17,0,0)
        self.config.noct.startTime = time(5,0,0)

        expected = [True,True,True,True,True,False,False,False,False,False,False,False,False,False,False,False,False,True,True,True,True,True,True,True]
        self.runTest(expected)

    def test_dayConfigDayIsDay(self):
        self.config.di.startTime = time(5,0,0)
        self.config.noct.startTime = time(17,0,0)

        expected = [False,False,False,False,False,True,True,True,True,True,True,True,True,True,True,True,True,False,False,False,False,False,False,False]
        self.runTest(expected)

    def test_dayConfigDayIsMidnight(self):
        self.config.di.startTime = time(0,0,0)
        self.config.noct.startTime = time(12,0,0)

        expected = [True,True,True,True,True,True,True,True,True,True,True,True,False,False,False,False,False,False,False,False,False,False,False,False]
        self.runTest(expected)

class DayConfigTest(unittest.TestCase):
    def test_export(self):
        config = DayConfig()
        config.di = ConfigDictMock('the day config')
        config.noct = ConfigDictMock('the night config')

        self.assertEqual(json.dumps(config.asDict()), "{\"day\": \"the day config\", \"night\": \"the night config\"}")
        # print json.dumps(config, cls=ConfigEncoder, indent=4)

if __name__ == '__main__':
    unittest.main()