from psireporter import Manager
from psistats2.plugins.reporters.cpu import CpuPerCore, CpuTotal
from psistats2.plugins.reporters.mem import MemoryReport
from psistats2.plugins.reporters.disk import DiskUsage
from psistats2.plugins.reporters.sensors import LmSensors
from psistats2.plugins.output.stdout import OutputStdout
from psistats2 import config
import time
import pprint

conf = config.load('psistats.conf')

manager = Manager(conf)
manager.start()

print('START')

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print('KEYBOARD STOP')
        break
    except Exception as e:
        print(e)
        break

print('END')

manager.stop()
