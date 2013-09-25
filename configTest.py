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

#if __name__ == '__main__':
 #   unittest.main()