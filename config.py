from datetime import datetime, time, timedelta
import json
import pickle

#
# data updater
#
class ConfigRunner(object):
    def __init__(self):
        self.runner = DayRunner()

    def UpdateTime(self, config, state):
        state.time = datetime.now()
        self.update(self, config, state)

    def update(self, config, state):
        self.runner.update(config.activeConfig, state)

class DayRunner(object):
    def __init__(self):
        self.runner = UrneRunner()

    def update(self, config, state):
        if config.di.startTime > config.noct.startTime:
            state.day = state.time.time() > config.di.startTime or state.time.time() < config.noct.startTime
        else:
            state.day = state.time.time() > config.di.startTime and state.time.time() < config.noct.startTime

        currentConfig = config.di if state.day else config.noct

        self.runner.update(currentConfig, state)

class UrneRunner(object):
    def __init__(self):
        self.pumpRunner = PeriodicRunner()
        self.fanRunner = TriggerRunner()
        self.brumRunner = TriggerRunner()

    def update(self, config, state):
        state.pump = self.pumpRunner.valueAtTime(config.pumpPeriod, state.time)
        state.fan = self.fanRunner.valueWithValue(config.fanTrigger, state.temp)
        state.brum = self.brumRunner.valueWithValue(config.brumTrigger, state.humidity)

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
     
class TriggerRunner(object):
    def __init__(self):
        self.previousValue = False
        self.isterezis = 0.5

    def valueWithValue(self, triggerConfig, value):
        if self.previousValue:
            result = value>triggerConfig.triggerValue-self.isterezis
        else:
            result = value>=triggerConfig.triggerValue+self.isterezis
        self.previousValue = result

        return result if triggerConfig.mode else not result

#
# data codecs
#

class ConfigEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.asDict();

class ConfigFile(object):
    def __init__(self, filename):
        self.filename = filename

    def save(self, obj):
        with open(self.filename, "wb") as f:
            pickle.dump(obj, f)

    def load(self):
        with open(self.filename, "rb") as f:
            return pickle.load(f)

# state storage
#
class RegisterState(object):
    def __init__(self):
        self.time = datetime.min

        self.temp = 0.0
        self.humidity = 0.0

        self.day = False
        self.pump = False
        self.fan = False
        self.brum = False

#
# data storage
#

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
        self.fanTrigger = TriggerConfig()
        self.brumTrigger = TriggerConfig()

    def asDict(self):
        return {'start':self.startTime.isoformat(),'pump':self.pumpPeriod.asDict(), 'fan':self.fanTrigger.asDict(), 'brum':self.brumTrigger.asDict()}

class PeriodicConfig(object):
    def __init__(self):
        self.period = timedelta()
        self.duration = timedelta()

    def asDict(self):
        return {'period':self.period.total_seconds(),'duration':self.duration.total_seconds()}

class TriggerConfig(object):
    def __init__(self):
        self.mode = True # True = Sup
        self.triggerValue = 0.0

    def asDict(self):
        return {'mode':self.mode,'value':self.triggerValue}
