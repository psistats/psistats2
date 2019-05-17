import sys
import os

DLL_NAME = 'OpenHardwareMonitorLib'
DLL_FILENAME = '%s.dll' % DLL_NAME
DLL_PATH     = os.path.dirname(os.path.realpath(__file__))

sys.path.append(DLL_PATH)

try:
    import clr
    clr.AddReference(DLL_NAME)
    clr.AddReference('System')
    from System import Enum
    from OpenHardwareMonitor.Hardware import Computer, ISensor, SensorType
    from System import Enum
except ImportError:
    pass

def get_type_name(type):
    typeName = Enum.GetName(SensorType, type)
    return typeName

def print_all_sensors():
    ohm = OpenHardwareMonitor(
        MainboardEnabled=True,
        FanControllerEnabled=True,
        CPUEnabled=True,
        RAMEnabled=True,
        GPUEnabled=True,
        HDDEnabled=True
    )
    ohm.init()
    ohm.update()

    rows = []

    for sensor in ohm.all_sensors():
        rows.append([str(sensor.Identifier), sensor.Name, get_type_name(sensor.SensorType)])

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

    ohm.close()


class OpenHardwareMonitor():

    SETTINGS = ['MainboardEnabled', 'CPUEnabled', 'RAMEnabled', 'GPUEnabled', 'FanControllerEnabled', 'HDDEnabled']

    def __init__(self, sensors):
        self.MainboardEnabled = sensors.get('MainboardEnabled', False)
        self.CPUEnabled = sensors.get('CPUEnabled', False)
        self.RAMEnabled = sensors.get('RAMEnabled', False)
        self.GPUEnabled = sensors.get('GPUEnabled', False)
        self.FanControllerEnabled = sensors.get('FanControllerEnabled', False)
        self.HDDEnabled = sensors.get('HDDEnabled', False)

        self.__comp = None

    def init(self):

        comp = Computer()

        for setting in OpenHardwareMonitor.SETTINGS:
            setattr(comp, setting, getattr(self, setting))


        comp.Open()
        self.__comp = comp

    def update(self):
        for hw in self.__comp.Hardware:
            hw.Update()

    def hardware(self):
        return self.__comp.Hardware

    def all_sensors(self):

        sensors = []

        for hw in self.__comp.Hardware:
            hw.Update()

            for sensor in hw.Sensors:
                sensors.append(sensor)

        return sensors

    def close(self):
        self.__comp.Close()
