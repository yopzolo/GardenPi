import unittest
import json

from datetime import datetime, time, timedelta

from config import ConfigRoot, ConfigRunner, RegisterState
from config import ConfigSet, SetRunner
from config import PeriodicConfig, PeriodicRunner

class SetRunnerMock(SetRunner):
    def __init__(self):
        self.config = 0

    def updateAtTime(self, config, state, time):
        self.config = config

class ConfigTest(unittest.TestCase):

    def setUp(self):
        pass

    def assertConfig(self, runner, date, state, expectedDay, config, expectedConfig):
        runner.updateAtTime(config, state, date)
        self.assertEqual(runner.runner.config, expectedConfig)
        self.assertEqual(state.day, expectedDay)        
 
    def test_configRoot(self):
        config = ConfigRoot()

        dayConfig = config.configSets[0]
        dayConfig.startTime = time(17,0,0)
        
        nightConfig = config.configSets[1]
        nightConfig.startTime = time(5,0,0)

        runner = ConfigRunner()
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
        
    def test_configSet(self):
        pass

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
        self.assertEqual(runner.valueAtTime(config, datetime(1981,11,2,17,0,0)), expected[0])
        self.assertEqual(runner.valueAtTime(config, datetime(1981,11,2,17,11,0)), expected[11])

if __name__ == '__main__':
    unittest.main()