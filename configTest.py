import unittest
import json
import string

from datetime import datetime, time, timedelta

from config import RegisterState
from config import ConfigEncoder, ConfigFile
from config import RootConfig, ConfigRunner
from config import DayConfig, DayRunner
from config import UrneConfig, UrneRunner
from config import PeriodicConfig, PeriodicRunner
from config import TriggerConfig, TriggerRunner

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

        # TODO remove file

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
        config.brumTrigger = ConfigDictMock('the brum')
        # config.pumpPeriod.period = timedelta(minutes = 15)
        # config.pumpPeriod.duration = timedelta(minutes = 5)

        self.assertEqual(json.dumps(config.asDict()), "{\"start\": \"05:00:00\", \"pump\": \"the pump\", \"fan\": \"the fan\", \"brum\": \"the brum\"}")
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