import unittest
import json
import string

from datetime import datetime, time, timedelta

from config import RegisterState
from config import DayConfig, DayRunner, DayEncoder
from config import UrneConfig, UrneRunner
from config import PeriodicConfig, PeriodicRunner

class SetRunnerMock(UrneRunner):
    def __init__(self):
        self.config = 0
        self.time = 0
        self.state = 0

    def updateAtTime(self, config, state, time):
        self.config = config
        self.state = state
        self.time = time

class ConfigRunnerTest(unittest.TestCase):

    def assertConfig(self, runner, date, state, expectedDay, config, expectedConfig):
        runner.updateAtTime(config, state, date)
        self.assertEqual(runner.runner.config, expectedConfig)
        self.assertEqual(runner.runner.time, date)
        self.assertEqual(runner.runner.state, state)
        self.assertEqual(state.day, expectedDay)        
 
    def test_dayConfig(self):
        config = DayConfig()

        dayConfig = config.di
        dayConfig.startTime = time(17,0,0)
        
        nightConfig = config.noct
        nightConfig.startTime = time(5,0,0)

        runner = DayRunner()
        runner.runner = SetRunnerMock()

        current = RegisterState()
        
        self.assertConfig(runner, datetime(1981,11,2,13,0,0), current, False, config, nightConfig)
        self.assertConfig(runner, datetime(1981,11,2,16,0,0), current, False, config, nightConfig)
        self.assertConfig(runner, datetime(1981,11,2,17,1,0), current, True, config, dayConfig)
        self.assertConfig(runner, datetime(1981,11,2,19,0,0), current, True, config, dayConfig)
        self.assertConfig(runner, datetime(1981,11,3,1,0,0), current, True, config, dayConfig)
        self.assertConfig(runner, datetime(1981,11,3,6,0,0), current, False, config, nightConfig)
        self.assertConfig(runner, datetime(1981,11,3,15,0,0), current, False, config, nightConfig)
        self.assertConfig(runner, datetime(1981,11,3,18,0,0), current, True, config, dayConfig)

    def test_dayConfig_weird(self):
        config = DayConfig()

        dayConfig = config.di
        dayConfig.startTime = time(11,0,0)
        
        nightConfig = config.noct
        nightConfig.startTime = time(5,0,0)

        runner = DayRunner()
        runner.runner = SetRunnerMock()

        current = RegisterState()
        
        # self.assertConfig(runner, datetime(1981,11,2,13,0,0), current, False, config, nightConfig)
        # self.assertConfig(runner, datetime(1981,11,2,16,0,0), current, False, config, nightConfig)
        # self.assertConfig(runner, datetime(1981,11,2,17,1,0), current, True, config, dayConfig)
        # self.assertConfig(runner, datetime(1981,11,2,19,0,0), current, True, config, dayConfig)
        # self.assertConfig(runner, datetime(1981,11,3,1,0,0), current, True, config, dayConfig)
        # self.assertConfig(runner, datetime(1981,11,3,6,0,0), current, False, config, nightConfig)
        # self.assertConfig(runner, datetime(1981,11,3,15,0,0), current, False, config, nightConfig)
        # self.assertConfig(runner, datetime(1981,11,3,18,0,0), current, True, config, dayConfig)

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

class ConfigRootTest(unittest.TestCase):
    def test_export(self):
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

        self.assertEqual(json.dumps(config, cls=DayEncoder), "{\"day\": {\"start\": \"05:00:00\", \"pump\": {\"duration\": 300.0, \"period\": 900.0}}, \"night\": {\"start\": \"17:00:00\", \"pump\": {\"duration\": 60.0, \"period\": 3600.0}}}")
        print json.dumps(config, cls=DayEncoder, indent=4)

class UrneConfigTest(unittest.TestCase):
    def test_dump(self):
        config = UrneConfig()
        config.startTime = time(5,0,0)
        config.pumpPeriod.period = timedelta(minutes = 15)
        config.pumpPeriod.duration = timedelta(minutes = 5)

        self.assertEqual(json.dumps(config.asDict()), "{\"start\": \"05:00:00\", \"pump\": {\"duration\": 300.0, \"period\": 900.0}}")

class PeriodicConfigTest(unittest.TestCase):
    def test_dump(self):
        config = PeriodicConfig()
        config.period = timedelta(minutes = 5)
        config.duration = timedelta(minutes = 2)

        self.assertEqual(json.dumps(config.asDict()), "{\"duration\": 120.0, \"period\": 300.0}")

if __name__ == '__main__':
    unittest.main()