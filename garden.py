# Imports
import webiopi
import time
import json
import string

from config import RegisterState
from config import RootConfig, ConfigRunner, ConfigEncoder
from datetime import time, timedelta

webiopi.setDebug()
GPIO    = webiopi.GPIO
LIGHT   = 23
PUMP    = 24

config  = RootConfig()
runner  = ConfigRunner()
current = RegisterState()

def setup():
    pass

def updateGPIO(pin, newValue):
    value = GPIO.digitalRead(pin)
    if not value==newValue:
        GPIO.digitalWrite(pin, newValue)

def loop():
    global current
    runner.update(config, current)

    # webiopi.debug(current.__dict__)

    updateGPIO(LIGHT, current.day)
    updateGPIO(PUMP, current.pump)
    
    webiopi.sleep(5)

def destroy():
    webiopi.debug("Script with macros - Destroy")

@webiopi.macro
def getButtons():
    return json.dumps({'ligth' : LIGHT, 'pump': PUMP, 'fan' : 21, 'brum' : 22})
    
@webiopi.macro
def setConfig(day_start, pump_duration_day, pump_period_day, night_start, pump_duration_night, pump_period_nigth):
    global config
    dayConfig = config.activeConfig.di

    timeValues = day_start.split(":")    
    dayConfig.startTime = time(int(timeValues[0]), int(timeValues[1]), int(timeValues[2]))

    pumpDayConfig = dayConfig.pumpPeriod
    pumpDayConfig.period = timedelta(seconds=int(pump_period_day))
    pumpDayConfig.duration = timedelta(seconds=int(pump_duration_day))
        
    nightConfig = config.activeConfig.noct

    timeValues = night_start.split(":")    
    nightConfig.startTime = time(int(timeValues[0]), int(timeValues[1]), int(timeValues[2]))

    pumpNigthConfig = nightConfig.pumpPeriod
    pumpNigthConfig.period = timedelta(seconds=int(pump_period_nigth))
    pumpNigthConfig.duration = timedelta(seconds=int(pump_duration_night))

    webiopi.debug(json.dumps(config, cls=ConfigEncoder))

@webiopi.macro
def getConfig():
    return json.dumps(config, cls=ConfigEncoder)
