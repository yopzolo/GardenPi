# Imports
import webiopi
import time
import json

from config import ConfigRoot, ConfigRunner, RegisterState
from datetime import time, timedelta

webiopi.setDebug()
GPIO    = webiopi.GPIO
LIGHT   = 23
PUMP    = 24

config  = ConfigRoot()
runner  = ConfigRunner()
current = RegisterState()

def setup():
    dayConfig = config.configSets[0]
    dayConfig.startTime = time(17,0,0)

    pumpDayConfig = dayConfig.pumpPeriod
    pumpDayConfig.period = timedelta(minutes=15)
    pumpDayConfig.duration = timedelta(minutes=5)
        
    nightConfig = config.configSets[1]
    nightConfig.startTime = time(5,0,0)

    pumpNigthConfig = nightConfig.pumpPeriod
    pumpNigthConfig.period = timedelta(hours=1)
    pumpNigthConfig.duration = timedelta(minutes=1)
    
    webiopi.debug("Script with macros - Setup")

def updateGPIO(pin, newValue):
    value = GPIO.digitalRead(pin)
    if not value==newValue:
        GPIO.digitalWrite(pin, newValue)

def loop():
    global current
    runner.update(config, current)

    #webiopi.debug(current.__dict__)

    updateGPIO(LIGHT, current.day)
    updateGPIO(PUMP, current.pump)

def destroy():
    webiopi.debug("Script with macros - Destroy")

@webiopi.macro
def getButtons():
    return json.dumps({'ligth' : LIGHT, 'pump': PUMP})

@webiopi.macro
def setConfig(ligth_start, ligth_duration, pump_cycle_day, pump_duration_day, pump_cycle_nigth, pump_duration_nigth, fan_trigger_temp_day, fan_trigger_temp_night):
    global duration;
    duration = int(ligth_duration);

@webiopi.macro
def getConfig():
	configLigth = {'ligth_start': 10, 'ligth_duration': 8};
	configPump = {'pump_cycle_day' : 30, 'pump_duration_day' : 30, 'pump_cycle_nigth' : 60, 'pump_duration_nigth' : 60}
	configFan = {'fan_trigger_temp_day' : 27 , 'fan_trigger_temp_night': 21};

	config = {'ligth' : configLigth, 'pump' : configPump, 'fan' : configFan};

	return json.dumps(config);