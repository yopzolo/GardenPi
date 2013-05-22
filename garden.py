# Imports
import webiopi
import time
import json

from config import ConfigRoot, ConfigRunner, RegisterState

webiopi.setDebug()
GPIO = webiopi.GPIO

duration = 1;

LIGHT   = 23

config = ConfigRoot()
runner = ConfigRunner()
curent = RegisterState()

def setup():
    dayConfig = config.configSets[0]
    dayConfig.startTime = time(17,0,0)

    pumpDayConfig = dayConfig.pumpPeriod
    pumpDayConfig.period = 15
    pumpDayConfig.duration = 5
        
    nightConfig = config.configSets[1]
    nightConfig.startTime = time(5,0,0)

    pumpNigthConfig = nightConfig.pumpPeriod
    pumpNigthConfig.period = 60
    pumpNigthConfig.duration = 1
    
    webiopi.debug("Script with macros - Setup")

def loop():
    runner.update(config, global state)

    print state.__dict__
    value = not GPIO.digitalRead(LIGHT)
    GPIO.digitalWrite(LIGHT, value)
    webiopi.sleep(duration)        

def destroy():
    webiopi.debug("Script with macros - Destroy")

@webiopi.macro
def getButtons():
    return json.dumps({'18': 18, '22': 22,'ligth' : 23, 'pump': 24, 'fan': 25})

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