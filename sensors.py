from psistats2.libsensors.lib import sensors as libsensors
import sys, time

feature_labels = {}
feature_labels[libsensors.SENSORS_FEATURE_ENERGY] = "SENSORS_FEATURE_ENERGY"
feature_labels[libsensors.SENSORS_FEATURE_BEEP_ENABLE] = "SENSORS_FEATURE_BEEP_ENABLE"
feature_labels[libsensors.SENSORS_FEATURE_IN] = "SENSORS_FEATURE_IN"
feature_labels[libsensors.SENSORS_FEATURE_FAN] = "SENSORS_FEATURE_FAN"
feature_labels[libsensors.SENSORS_FEATURE_VID] = "SENSORS_FEATURE_VID"
feature_labels[libsensors.SENSORS_FEATURE_CURR] = "SENSORS_FEATURE_CURR"
feature_labels[libsensors.SENSORS_FEATURE_TEMP] = "SENSORS_FEATURE_TEMP"
feature_labels[libsensors.SENSORS_FEATURE_POWER] = "SENSORS_FEATURE_POWER"
feature_labels[libsensors.SENSORS_FEATURE_HUMIDITY] = "SENSORS_FEATURE_HUMIDITY"
feature_labels[libsensors.SENSORS_FEATURE_INTRUSION] = "SENSORS_FEATURE_INTRUSION"

feature_units = {}
feature_units[libsensors.SENSORS_FEATURE_FAN] = "RPM"
feature_units[libsensors.SENSORS_FEATURE_TEMP] = "C"

###
#
# config:
#
# features: ['feature:subfeature']
#
###
def main():
    for chip in libsensors.iter_detected_chips():
        confKey = str(chip)

        for feature in chip:

            if feature.type in feature_labels:
                featureName = feature_labels[feature.type]
            else:
                featureName = 'Unknown Feature'

            if feature.type in feature_units:
                unit = feature_units[feature.type]
            else:
                unit = '?'

            v = None
            try:
                v = feature.get_value()
            except libsensors.SensorsError:
                v = 'cant read this sensor'

            sys.stdout.write('%s.%s (%s %s)\n' % (confKey, featureName, v, unit))

            for subfeature in feature:
                print('%s: %s' % (subfeature.name, subfeature.get_value()))

            print('---')


class LMSensors():

    def __init__(self, features):
        self.features = features
        self.__features = []

    def init(self):
        libsensors.init()

        chips = libsensors.iter_detected_chips()

        for chip in chips:
            confKey = str(chip)

            for feature in chip:
                for subfeature in feature:
                    featureName = '%s:%s' % (confKey, subfeature.name.decode('utf-8'))

                    print("feature name: %s" % featureName)

                    if featureName in self.features:
                        self.__features.append((featureName, subfeature))

    def values(self):
        return [(fname, sf.get_value()) for fname, sf in self.__features]

lms = LMSensors((
    'coretemp-isa-0000:temp1_input',
    'coretemp-isa-0000:temp2_input',
    'coretemp-isa-0000:temp3_input',
    'coretemp-isa-0000:temp4_input'
))

lms.init()

while True:
    print(lms.values())
    time.sleep(1)
