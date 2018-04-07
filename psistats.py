from psireporter import Manager
from psistats2.plugins.reporters.cpu import CpuPerCore, CpuTotal
from psistats2.plugins.reporters.mem import MemoryReport
from psistats2.plugins.reporters.disk import DiskUsage
from psistats2.plugins.reporters.sensors import LmSensors
from psistats2.plugins.output.stdout import OutputStdout
import time
config = {
    'reporters': {
        'cpu_per_core': {
            'interval': 1
        },
        'cpu_total': {
            'interval': 1,
            'enabled': False
        },
        'memory': {
            'interval': 10
        },
        'disk_usage': {
            'interval': 30,
            'settings': {
                'disks': ['c:/','d:/']
            }
        },
        'lm_sensors': {
            'interval': 5,
            'enabled': False,
            'settings': {
                'features': [
                    'coretemp-isa-0000:temp1_input',
                    'coretemp-isa-0000:temp2_input',
                    'coretemp-isa-0000:temp3_input',
                    'coretemp-isa-0000:temp4_input'
                ]
            }
        },
        'openhardwaremonitor': {
            'interval': 5,
            'enabled': True
        }
    }
}

manager = Manager(config)

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