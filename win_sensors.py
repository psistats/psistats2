import sys, clr
import time
dll_path = 'C:\\Users\\v0idnull\\Documents\\GitHub\\openhardwaremonitor\\Bin\\Debug'
dll_file = 'OpenHardwareMonitorLib.dll'

sys.path.append(dll_path)

clr.AddReference('OpenHardwareMonitorLib')
clr.AddReference('System')
from OpenHardwareMonitor.Hardware import Computer, HardwareEventHandler, ISensor, SensorType
from System import Enum

def HardwareAdded(hardware):
    print("Hardware added!")
    
def HardwareRemoved(hardware):
    print("Hardware removed!")


sensors = [
    '/intelcpu/0/temperature/0',
    '/intelcpu/0/temperature/1',
    '/intelcpu/0/temperature/2',
    '/intelcpu/0/temperature/3'
]

hardware = [
    '/intelcpu/0'
]

__sensors = []
__hw = []
    
    
comp = Computer()

comp.MainboardEnabled = False
comp.RAMEnabled = False
comp.CPUEnabled = True
comp.GPUEnabled = False
comp.HDDEnabled = False
comp.Open()

for hw in comp.Hardware:
    print(hw.Identifier, hardware)
    if str(hw.Identifier) in hardware:
        __hw.append(hw)

        hw.Update()
        for sensor in hw.Sensors:
            if str(sensor.Identifier) in sensors:
                __sensors.append(sensor)

while True:

    try:
        for hw in __hw:
            hw.Update()
            for sensor in __sensors:
            
                typeName = Enum.GetName(SensorType, sensor.SensorType)
                
                print("name: %s - sensor: %s - type: %s - value: %s" % (sensor.Name, sensor.Identifier, typeName, sensor.Value))
            
        print('---')
        time.sleep(1)
    except KeyboardInterrupt:
        break

comp.Close()