from psistats2.libsensors.lib import sensors as lmsensors
import sys, os

def print_all_sensors():

    print('-' * 80)
    print('List of all available sensors')
    print('')
    print('Use the idenifier when configuring which sensors to report.')
    print('')

    lm = LibSensors()
    lm.init()

    rows = []

    for sensor in lm.sensors:
        rows.append([sensor.identifier, sensor.label, sensor.type])

    col_widths = [max([len(col[0]) for col in rows]) + 2, max([len(col[1]) for col in rows]) + 2]

    sys.stdout.write('Identifier'.ljust(col_widths[0]))
    sys.stdout.write('Name'.ljust(col_widths[1]))
    sys.stdout.write('Type')
    sys.stdout.write(os.linesep)
    sys.stdout.write('-' * 80)
    sys.stdout.write(os.linesep)

    for row in rows:
        for idx, col in enumerate(row):
            if idx < 2:
                sys.stdout.write(col.ljust(col_widths[idx]))
            else:
                sys.stdout.write(col)
        sys.stdout.write(os.linesep)


class Sensor():
    def __init__(self, chip, feature, sensor):
        self._feature = feature
        self._sensor = sensor
        self._chip = chip
        self._identifier = '%s:%s' % (str(chip), self._sensor.name.decode('utf-8'))
        self._label = '%s' % (self._feature.label)

    @property
    def type(self):
        return LibSensors.TYPES[self._feature.type]

    @property
    def value(self):
        return self._sensor.get_value()

    @property
    def identifier(self):
        return self._identifier

    @property
    def label(self):
        return self._label

class LibSensors():

    TYPES = dict([
        (lmsensors.SENSORS_FEATURE_ENERGY, 'ENERGY'),
        (lmsensors.SENSORS_FEATURE_BEEP_ENABLE, 'BEEP_ENABLE'),
        (lmsensors.SENSORS_FEATURE_IN, 'IN'),
        (lmsensors.SENSORS_FEATURE_FAN, 'FAN'),
        (lmsensors.SENSORS_FEATURE_VID, 'VID'),
        (lmsensors.SENSORS_FEATURE_CURR, 'CURR'),
        (lmsensors.SENSORS_FEATURE_TEMP, 'TEMP'),
        (lmsensors.SENSORS_FEATURE_POWER, 'POWER'),
        (lmsensors.SENSORS_FEATURE_HUMIDITY, 'HUMIDITY'),
        (lmsensors.SENSORS_FEATURE_INTRUSION, 'INTRUSION')
    ])

    def __init__(self, identifiers=None):

        if identifiers is None:
            self.identifiers = []
        else:
            self.identifiers = identifiers

        self.initialized = False
        self.__sensors = []


    def init(self):
        lmsensors.init()

        chips = lmsensors.iter_detected_chips()
        for chip in chips:
            confKey = str(chip)

            for feature in chip:
                for subfeature in feature:
                    identifier = '%s:%s' % (confKey, subfeature.name.decode('utf-8'))

                    if len(self.identifiers) is 0 or identifier in self.identifiers:
                        self.__sensors.append(Sensor(chip, feature, subfeature))

        self.initialized = True

    @property
    def sensors(self):
        return self.__sensors

    def sensor_values(self):
        return [(sensor.identifier, sensor.type, sensor.value) for sensor in self.__sensors]



