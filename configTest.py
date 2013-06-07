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
from config import RootConfig, ConfigRunner
from config import DayConfig, DayRunner
from config import UrneConfig, UrneRunner
from config import PeriodicConfig, PeriodicRunner
from config import TriggerConfig, TriggerRunner
from config import DelayRunner

class ConfigRunnerTest(unittest.TestCase):

    def test_run_active_config(self):
        config = RootConfig();
        config.configs = [DayConfig(), DayConfig(), DayConfig()]
        config.activeConfig = config.configs[1]

        current = RegisterState()
        current.time = datetime.now()

        runner = ConfigRunner()
        runner.runner = RunnerMock()

        runner.update(config, current)
        
        self.assertEqual(runner.runner.config, config.configs[1])
        self.assertEqual(runner.runner.state, current)
       
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

class DelayRunnerTest(unittest.TestCase):
    def test_delay(self):
        runner = DelayRunner(timedelta(minutes = 1));

        self.assertEqual(runner.valueWithValueAtTime(False, datetime(1981,11,2,17,0,0)), False)
        self.assertEqual(runner.valueWithValueAtTime(False, datetime(1981,11,2,17,1,0)), False)
        self.assertEqual(runner.valueWithValueAtTime(True, datetime(1981,11,2,17,1,30)), False)
        self.assertEqual(runner.valueWithValueAtTime(True, datetime(1981,11,2,17,02,01)), False)
        self.assertEqual(runner.valueWithValueAtTime(True, datetime(1981,11,2,17,03,00)), True)
        self.assertEqual(runner.valueWithValueAtTime(False, datetime(1981,11,2,17,04,01)), False)
        self.assertEqual(runner.valueWithValueAtTime(True, datetime(1981,11,2,17,05,00)), False)
        self.assertEqual(runner.valueWithValueAtTime(True, datetime(1981,11,2,17,05,59)), False)
        self.assertEqual(runner.valueWithValueAtTime(True, datetime(1981,11,2,17,06,30)), True)
        self.assertEqual(runner.valueWithValueAtTime(True, datetime(1981,11,2,19,06,30)), True)

class ConfigFileTest(unittest.TestCase):
    def test_fileDontExists(self):
        loader = ConfigFile('ConfigFileTest_test_fileDontExists.pyc')
        try:
            loadedConfig = loader.load()
            self.fail()
        except IOError:
            pass

    def test_pickle(self):
        config = DayConfig()

        dayConfig = config.di
        dayConfig.startTime = time(5,0,0)
        pumpConfig = dayConfig.pumpPeriod
        pumpConfig.period = timedelta(minutes = 15)
        pumpConfig.duration = timedelta(minutes = 5)
        
        nigthConfig = config.noct
        nigthConfig.startTime = time(17,0,0)
        pumpConfig = nigthConfig.pumpPeriod
        pumpConfig.period = timedelta(minutes = 60)
        pumpConfig.duration = timedelta(minutes = 1)

        saver = ConfigFile('ConfigFileTest_test_pickle.pyc')
        saver.save(config)

        # TODO assert file exists

        loader = ConfigFile('ConfigFileTest_test_pickle.pyc')
        loadedConfig = loader.load()

        os.unlink('ConfigFileTest_test_pickle.pyc')

        loadedDayConfig = loadedConfig.di
        self.assertEqual(loadedDayConfig.startTime, time(5,0,0))
        loadedPumpConfig = loadedDayConfig.pumpPeriod
        self.assertEqual(loadedPumpConfig.period, timedelta(minutes = 15))
        self.assertEqual(loadedPumpConfig.duration, timedelta(minutes = 5))
        
        # print json.dumps(config, cls=ConfigEncoder, indent=4)

class ConfigDictMock(object):
    def __init__(self, name):
        self.name = name

    def asDict(self):
        return self.name;

class DayConfigTest(unittest.TestCase):
    def test_export(self):
        config = DayConfig()
        config.di = ConfigDictMock('the day config')
        config.noct = ConfigDictMock('the night config')

        self.assertEqual(json.dumps(config.asDict()), "{\"day\": \"the day config\", \"night\": \"the night config\"}")
        # print json.dumps(config, cls=ConfigEncoder, indent=4)

class UrneConfigTest(unittest.TestCase):
    def test_dump(self):
        config = UrneConfig()
        config.startTime = time(5,0,0)
        config.pumpPeriod = ConfigDictMock('the pump')
        config.fanTrigger = ConfigDictMock('the fan')
        config.fanHighTrigger = ConfigDictMock('the fan High speed')
        config.brumTrigger = ConfigDictMock('the brum')
        # config.pumpPeriod.period = timedelta(minutes = 15)
        # config.pumpPeriod.duration = timedelta(minutes = 5)

        self.assertEqual(json.dumps(config.asDict()), "{\"start\": \"05:00:00\", \"pump\": \"the pump\", \"brum\": \"the brum\", \"fan\": \"the fan\", \"fan_high\": \"the fan High speed\"}")
        # print json.dumps(config, cls=ConfigEncoder, indent=4)

class PeriodicConfigTest(unittest.TestCase):
    def test_dump(self):
        config = PeriodicConfig()
        config.period = timedelta(minutes = 5)
        config.duration = timedelta(minutes = 2)

        self.assertEqual(json.dumps(config.asDict()), "{\"duration\": 120.0, \"period\": 300.0}")
        # print json.dumps(config, cls=ConfigEncoder, indent=4)
class TriggerConfigTest(unittest.TestCase):
    def test_dump(self):
        config = TriggerConfig()
        config.mode = True;
        config.triggerValue = 25.0

        self.assertEqual(json.dumps(config.asDict()), "{\"mode\": true, \"value\": 25.0}")

class RegisterStateLoggerTest(unittest.TestCase):
    def test_log(self):
        state = RegisterState()
        state.time = datetime(1981, 11, 2, 12, 15, 58)
        state.temp = 26.0
        state.humidity = 55.0
        state.day = True
        state.pump = True
        state.fan = False
        state.brum = False

        logger = RegisterStateLogger('RegisterStateLoggerTest_test_log.txt', timedelta(seconds = 30))
        logger.log(state)

        state.time = datetime(1981, 11 ,2 , 12 ,16, 00)
        logger.log(state)

        actual1 = ""
        with open('RegisterStateLoggerTest_test_log.txt') as logFile:
            actual1 = logFile.read()

        state.temp = 25.5
        state.humidity = 54.0
        state.day = False
        state.pump = False
        state.fan = True
        state.brum = True

        state.time = datetime(1981, 11, 2, 12, 16, 05)
        logger.log(state)
        
        state.time = datetime(1981, 11, 2, 12, 16, 15)
        logger.log(state)
        
        state.time = datetime(1981, 11, 2, 12, 16, 25)
        logger.log(state)

        state.time = datetime(1981, 11, 2, 12, 16, 35)
        logger.log(state)

        state.time = datetime(1981, 11, 2, 12, 16, 45)
        logger.log(state)

        actual2 = ""
        with open('RegisterStateLoggerTest_test_log.txt') as logFile:
           actual2 = logFile.read()

        os.remove("RegisterStateLoggerTest_test_log.txt")

        self.assertEqual(actual1, "1981-11-02T12:15:58,26.0,55.0,True,True,False,False,False\n")
        self.assertEqual(actual2, "1981-11-02T12:15:58,26.0,55.0,True,True,False,False,False\n1981-11-02T12:16:35,25.5,54.0,False,False,True,False,True\n")

        #TODO creer un fichier et valider qu'on append correctement

class RunnerMock(UrneRunner):
    def __init__(self):
        self.config = 0
        self.time = 0
        self.state = 0

    def update(self, config, state):
        self.config = config
        self.state = state

if __name__ == '__main__':
    unittest.main()