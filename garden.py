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

# Imports
import webiopi
import time
import json
import string

from config import RegisterState, RegisterStateLogger
from RootRunner import RootConfig, RootRunner
from config import ConfigEncoder, ConfigFile
from datetime import time, timedelta

# webiopi.setDebug()
GPIO    = webiopi.GPIO

LIGHT   = 23
PUMP    = 24

FAN     = 25
FANHIGH = 18

BRUM    = 22
BRUMFAN = 27

config = False
# = RootConfig()
runner  = RootRunner()
current = RegisterState()
logger = RegisterStateLogger('./GardenPy_Logs.txt', timedelta(minutes=5))

def setup():
    webiopi.debug("Loading config")
    global config
    try:
        config = ConfigFile('GardenPyConfig.pyc').load()
    except (IOError, UnicodeDecodeError):
        config = RootConfig()


def updateGPIO(pin, newValue):
    value = GPIO.digitalRead(pin)
    if value==newValue:
        GPIO.digitalWrite(pin, not newValue)

def loop():
    global current

    temp = webiopi.deviceInstance("temp1")

    current.temp = temp.getCelsius()
    current.humidity = temp.getHumidity()

#    webiopi.debug(current.temp)

    runner.updateTime(config, current)

    updateGPIO(LIGHT, current.day)
    updateGPIO(PUMP, current.pump)

    updateGPIO(FAN, current.fan)
    updateGPIO(FANHIGH, current.fanHigh)

    updateGPIO(BRUM, current.brum)
    updateGPIO(BRUMFAN, current.brumFan)
    
    logger.log(current)

    webiopi.sleep(5)

def destroy():
    webiopi.debug("Saving config")
    ConfigFile('GardenPyConfig.pyc').save(config)
    
@webiopi.macro
def getButtons():
    return json.dumps({'ligth' : LIGHT, 'pump': PUMP, 'fan' : FAN, 'fan_high' : FANHIGH, 'brum' : BRUM})
    
def isTrue(strValue):
    return strValue in ['true', 'True', '1', 't', 'T', 'Y', 'y', 'yes', 'YES']

@webiopi.macro
def setConfig(day_start, pump_duration_day, pump_period_day,  brum_mode_value_day, brum_trigger_value_day, fan_mode_value_day, fan_trigger_value_day, fan_high_mode_value_day, fan_high_trigger_value_day, night_start, pump_duration_night, pump_period_nigth, brum_mode_value_nigth, brum_trigger_value_nigth, fan_mode_value_nigth, fan_trigger_value_nigth, fan_high_mode_value_nigth, fan_high_trigger_value_nigth):
    global config
    dayConfig = config.activeConfig.di

    timeValues = day_start.split(":")    
    dayConfig.startTime = time(int(timeValues[0]), int(timeValues[1]), int(timeValues[2]))

    pumpDayConfig = dayConfig.pumpPeriod
    pumpDayConfig.period = timedelta(seconds=int(pump_period_day))
    pumpDayConfig.duration = timedelta(seconds=int(pump_duration_day))
        
    fanDayConfig = dayConfig.fanTrigger
    fanDayConfig.triggerValue = float(fan_trigger_value_day)
    fanDayConfig.mode = isTrue(fan_mode_value_day)

    fanHighDayConfig = dayConfig.fanHighTrigger
    fanHighDayConfig.triggerValue = float(fan_high_trigger_value_day)
    fanHighDayConfig.mode = isTrue(fan_high_mode_value_day)

    brumDayConfig = dayConfig.brumTrigger
    brumDayConfig.triggerValue = float(brum_trigger_value_day)
    brumDayConfig.mode = isTrue(brum_mode_value_day)

    nightConfig = config.activeConfig.noct

    timeValues = night_start.split(":")    
    nightConfig.startTime = time(int(timeValues[0]), int(timeValues[1]), int(timeValues[2]))

    pumpNigthConfig = nightConfig.pumpPeriod
    pumpNigthConfig.period = timedelta(seconds=int(pump_period_nigth))
    pumpNigthConfig.duration = timedelta(seconds=int(pump_duration_night))

    fanNightConfig = nightConfig.fanTrigger
    fanNightConfig.triggerValue = float(fan_trigger_value_nigth)
    fanNightConfig.mode = isTrue(fan_mode_value_nigth)

    fanHighNigthConfig = nightConfig.fanHighTrigger
    fanHighNigthConfig.triggerValue = float(fan_high_trigger_value_nigth)
    fanHighNigthConfig.mode = isTrue(fan_high_mode_value_nigth)

    brumNightConfig = nightConfig.brumTrigger
    brumNightConfig.triggerValue = float(brum_trigger_value_nigth)
    brumNightConfig.mode = isTrue(brum_mode_value_nigth)
    
 #   webiopi.debug(json.dumps(config, cls=ConfigEncoder))

@webiopi.macro
def getConfig():
    return json.dumps(config, cls=ConfigEncoder)
