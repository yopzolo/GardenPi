from datetime import datetime, time, timedelta
import json

#
# data updater
#

class ConfigRunner(object):
    def __init__(self):
        self.runner = DayRunner()

    def update(self, config, state):
        self.updateAtTime(config, state, datetime.now())

    def updateAtTime(self, config, state, time):
        self.runner.updateAtTime(config.activeConfig, state, time)

class DayRunner(object):

    def __init__(self):
        self.runner = UrneRunner()

    def update(self, config, state):
        self.updateAtTime(config, state, datetime.now())

    def updateAtTime(self, config, state, time):
        if time.time() > config.di.startTime or time.time() < config.noct.startTime:
            currentConfig = config.di
            state.day = True
        else:
            currentConfig = config.noct
            state.day = False;

        self.runner.updateAtTime(currentConfig, state, time)

class UrneRunner(object):
    def __init__(self):
        self.pumpRunner = PeriodicRunner()

    def updateAtTime(self, config, state, time):
        state.pump = self.pumpRunner.valueAtTime(config.pumpPeriod, time)

class PeriodicRunner(object):
    def __init__(self):
        self.lastOn = datetime(1970,1,1,0,0,0)

    def valueAtTime(self, periodicConfig, time):
        if time >= self.lastOn + periodicConfig.period:
            self.lastOn = time
            return True
        if time >= self.lastOn + periodicConfig.duration:
            return False
            
        return True;
     

# state storage
#
class RegisterState(object):
    def __init__(self):
        self.day = False
        self.pump = False

#
# data storage
#

class ConfigEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.asDict();

class RootConfig(object):
    def __init__(self):
        self.configs = [DayConfig()]
        self.activeConfig = self.configs[0]
    
    def asDict(self):
        return self.activeConfig.asDict()

class DayConfig(object):
    def __init__(self):
        self.di = UrneConfig();
        self.noct = UrneConfig();

    def asDict(self):
        return {'day':self.di.asDict(),'night':self.noct.asDict()}

class UrneConfig(object):
    def __init__(self):
        self.startTime = time.min
        self.pumpPeriod = PeriodicConfig()

    def asDict(self):
        return {'start':self.startTime.isoformat(),'pump':self.pumpPeriod.asDict()}

class PeriodicConfig(object):
    def __init__(self):
        self.period = timedelta()
        self.duration = timedelta()

    def asDict(self):
        return {'period':self.period.total_seconds(),'duration':self.duration.total_seconds()}
