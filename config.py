from datetime import datetime, time, timedelta
import json
#
# data updater
#
class ConfigRunner(object):

    def __init__(self):
        self.runner = SetRunner()

    def update(self, config, state):
        self.updateAtTime(config, state, datetime.now())

    def updateAtTime(self, config, state, time):
        if time.time() > config.configSets[0].startTime or time.time() < config.configSets[1].startTime:
            currentConfig = config.configSets[0]
            state.day = True
        else:
            currentConfig = config.configSets[1]
            state.day = False;

        self.runner.updateAtTime(currentConfig, state, time)

class SetRunner(object):
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

class RootEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.asDict();

class ConfigRoot(object):
    def __init__(self):
        self.configSets = [ConfigSet(), ConfigSet()]

    def asDict(self):
        return [self.configSets[0].asDict(),self.configSets[1].asDict()]

class ConfigSet(object):
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
