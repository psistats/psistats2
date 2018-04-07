from psistats2.libsensors.lib import sensors as libsensors
from psireporter import ReporterPlugin

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

