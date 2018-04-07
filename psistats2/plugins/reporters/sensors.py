try:
    from psistats2.libsensors.lib import sensors as libsensors
except:
    pass

from psistats2.openhardwaremonitor.openhardwaremonitor import OpenHardwareMonitor
    
from psireporter import ReporterPlugin    

class OHMReporter(metaclass=ReporterPlugin):

    PLUGIN_ID = 'openhardwaremonitor'
    
    def  __init__(self):
        self.initialized = False
        self.ohm = OpenHardwareMonitor(CPUEnabled=True)
        
    def init(self):
        self.ohm.init()
        self.initialized = True
        
    def report(self):
        if self.initialized is False:
            self.init()
        self.ohm.update()
        return "ohhhhmmmmm"
                
        
class LmSensors(metaclass=ReporterPlugin):

    PLUGIN_ID = 'lm_sensors'

    def __init__(self):
        self.sensors_initialized = False
        self.__features = []

    def init(self):
        libsensors.init()

        chips = libsensors.iter_detected_chips()

        for chip in chips:
            confKey = str(chip)

            for feature in chip:
                for subfeature in feature:
                    featureName = '%s:%s' % (confKey, subfeature.name.decode('utf-8'))

                    if featureName in self.config['features']:
                        self.__features.append((featureName, subfeature))

        self.sensors_initialized = True

    def report(self):
        if self.sensors_initialized == False:
            self.init()

        return [(fname, sf.get_value()) for fname, sf in self.__features]

