import os
from psistats2.openhardwaremonitor.openhardwaremonitor import OpenHardwareMonitor
from psistats2.openhardwaremonitor.openhardwaremonitor import get_type_name
from psistats2.reporter import PsistatsReporterPlugin

try:
    from psistats2.libsensors.libsensors import LibSensors
except:  # noqa: E722
    pass


class Sensors(PsistatsReporterPlugin):

    PLUGIN_ID = "sensors"

    def __init__(self, config):
      super(Sensors, self).__init__(config)
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

    def __init__(self, config):
        self.config = config
        self.initialized = False

        kwargs = {}

        print(self.config)

        for setting in OpenHardwareMonitor.SETTINGS:
            enabled = self.config[setting.lower()]

            if enabled == 'yes':
                kwargs[setting] = True
            else:
                kwargs[setting] = False
        
        


        self.ohm = OpenHardwareMonitor(kwargs)

    def init(self):
        self.ohm.init()
        self.initialized = True

    def report(self):
        if self.initialized is False:
            self.init()
        #self.ohm.update()
        return [(str(sensor.Identifier), get_type_name(sensor.SensorType), sensor.Value) for sensor in self.ohm.all_sensors() if str(sensor.Identifier) in self.config['sensors']]


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
        if self.sensors_initialized is False:
            self.init()
        return self._libsensors.sensor_values()
        