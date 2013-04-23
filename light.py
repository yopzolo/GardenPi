# Imports
import webiopi
import time
import json

webiopi.setDebug()
GPIO = webiopi.GPIO

duration = 1;

LIGHT   = 23

def setup():
    webiopi.debug("Script with macros - Setup")

def loop():
    value = not GPIO.digitalRead(LIGHT)
    GPIO.digitalWrite(LIGHT, value)
    webiopi.sleep(duration)        

def destroy():
    webiopi.debug("Script with macros - Destroy")



@webiopi.macro
def setConfig(inDuration):
    global duration;
    duration = int(inDuration);

@webiopi.macro
def getConfig():

	configLigth = {'ligth_start': 10, 'ligth_duration': 8};
	configPump = {'pump_cycle_day' : 30, 'pump_duration_day' : 30, 'pump_cycle_nigth' : 60, 'pump_duration_nigth' : 60}
	
	config = [configLigth, configPump];
		
	return json.dumps(config);