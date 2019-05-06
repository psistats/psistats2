import os


try:
    from psistats2.libsensors.libsensors import LibSensors
except:
    pass

from psistats2.openhardwaremonitor.openhardwaremonitor import OpenHardwareMonitor, print_all_sensors
from psistats2.reporter import ReporterPlugin


class SensorReporter(metaclass=ReporterPlugin):

    PLUGIN_ID = "sensors"

    def __init__(self):
        self.initialized = False

    def init(self):
        if os.name == 'nt':
            self._reporter = OHMReporter(self.config)
        else:
            self._reporter = LmSensors(self.config)

        self._reporter.init()
        self.initialized = True

    def report(self):
        if self.initialized is False:
            self.init()
        return self._reporter.report()


class OHMReporter():

    def  __init__(self, config):
        self.config = config
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


class LmSensors():

    def __init__(self, config):
        self.config = config
        self.sensors_initialized = False
        self._libsensors = None

    def init(self):
        self._libsensors = LibSensors(identifiers=self.config['sensors'])
        self._libsensors.init()

        self.sensors_initialized = True

    def report(self):
        if self.sensors_initialized == False:
            self.init()
        return self._libsensors.sensor_values()

#        return [(fname, sf.get_value()) for fname, sf in self.__features]

