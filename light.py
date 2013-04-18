# Imports
import webiopi
import time

webiopi.setDebug()
GPIO = webiopi.GPIO

LIGHT   = 23

def setup():
    webiopi.debug("Script with macros - Setup")

def loop():
    value = not GPIO.digitalRead(LIGHT)
    GPIO.digitalWrite(LIGHT, value)
    webiopi.sleep(5)        

def destroy():
    webiopi.debug("Script with macros - Destroy")
