import sys
import os
try:
    import clr
except:
    pass

DLL_NAME = 'OpenHardwareMonitorLib'    
DLL_FILENAME = '%s.dll' % DLL_NAME
DLL_PATH     = os.path.dirname(os.path.realpath(__file__))

class OpenHardwareMonitor():

    def __init__(self, **kwargs):
        self.MainboardEnabled = kwargs.get('MainboardEnabled', False)
        self.CPUEnabled = kwargs.get('CPUEnabled', False)
        self.RAMEnabled = kwargs.get('RAMEnabled', False)
        self.GPUEnabled = kwargs.get('GPUEnabled', False)
        self.FanControllerEnabled = kwargs.get('FanControllerEnabled', False)
        self.HDDEnabled = kwargs.get('HDDEnabled', False)
        
        self.__comp = None
        
    def init(self):
        
        sys.path.append(DLL_PATH)
        
        clr.AddReference(DLL_NAME)
        clr.AddReference('System')
        
        from OpenHardwareMonitor.Hardware import Computer, ISensor, SensorType
        from System import Enum
        
        comp = Computer()
        
        for setting in ['MainboardEnabled', 'CPUEnabled', 'RAMEnabled', 'GPUEnabled', 'FanControllerEnabled', 'HDDEnabled']:
            setattr(comp, setting, getattr(self, setting))
        
        
        comp.Open()
        self.__comp = comp
        
    def update(self):
        for hw in self.__comp.Hardware:
            hw.Update()