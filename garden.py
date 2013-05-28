# Imports
import webiopi
import time
import json
import string

from config import RegisterState
from config import RootConfig, ConfigRunner, ConfigEncoder, ConfigFile
from datetime import time, timedelta

# webiopi.setDebug()
GPIO    = webiopi.GPIO
LIGHT   = 23
PUMP    = 24
FAN     = 25
BRUM    = 22

config = False
# = RootConfig()
runner  = ConfigRunner()
current = RegisterState()

def setup():
    webiopi.debug("Loading config")
    global config
    try:
        config = ConfigFile('GardenPyConfig.pyc').load()
    except (IOError, UnicodeDecodeError):
        config = RootConfig()


def updateGPIO(pin, newValue):
    value = GPIO.digitalRead(pin)
    if not value==newValue:
        GPIO.digitalWrite(pin, newValue)

def loop():
    global current

    dht11 = webiopi.deviceInstance("dht11")

    current.temp = dht11.getCelsius()
    current.humidity = dht11.getHumidity()

#    webiopi.debug(current.temp)

    runner.update(config, current)

    updateGPIO(LIGHT, current.day)
    updateGPIO(PUMP, current.pump)
    updateGPIO(FAN, current.fan)
    updateGPIO(BRUM, current.brum)
    
    webiopi.sleep(5)

def destroy():
    webiopi.debug("Saving config")
    ConfigFile('GardenPyConfig.pyc').save(config)
    
@webiopi.macro
def getButtons():
    return json.dumps({'ligth' : LIGHT, 'pump': PUMP, 'fan' : FAN, 'brum' : BRUM})
    
def isTrue(strValue):
    return strValue in ['true', '1', 't', 'y', 'yes']

@webiopi.macro
def setConfig(day_start, pump_duration_day, pump_period_day, fan_mode_value_day, fan_trigger_value_day, brum_mode_value_day, brum_trigger_value_day, night_start, pump_duration_night, pump_period_nigth, fan_mode_value_nigth, fan_trigger_value_nigth, brum_mode_value_nigth, brum_trigger_value_nigth):
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

    brumNightConfig = nightConfig.brumTrigger
    brumNightConfig.triggerValue = float(brum_trigger_value_nigth)
    brumNightConfig.mode = isTrue(brum_mode_value_nigth)
    
 #   webiopi.debug(json.dumps(config, cls=ConfigEncoder))

@webiopi.macro
def getConfig():
    return json.dumps(config, cls=ConfigEncoder)
