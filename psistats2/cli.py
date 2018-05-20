from docopt import docopt
import os
import logging
from logging.config import fileConfig
from psistats2 import config
from psistats2.report import PsistatsReport
from psistats2.plugins.reporters.network import print_all_ifaces
import time
from psireporter import Manager
__doc__ = """psistats2

Usage:
    psistats start [options]
    psistats stop [options]
    psistats console [options]
    psistats ifaces [options]
    psistats sensors [options]
    psistats -h | --help
    psistats --version

Options:
    --debug        Enable debug logging
    --config=<fn>  Location of the config file
    -h --help      Display this help
    --version      Display the version
"""

def list_ifaces():
    print_all_ifaces()

def list_sensors():
    if os.name is 'nt':
        from psistats2.openhardwaremonitor.openhardwaremonitor import print_all_sensors
    else:
        from psistats2.libsensors.libsensors import print_all_sensors
    print_all_sensors()

def start():
    print('Not implemented yet')

def stop():
    print('Not implemented yet')

def console(conf):
    manager = Manager(conf, reportClass=PsistatsReport)
    manager.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        manager.stop()


def main(argv):
    arguments = docopt(__doc__, argv=argv, version='psistats2 v0.0.1')

    conffile = arguments['--config'] if arguments['--config'] is not None else 'psistats.conf'

    conf = config.load(conffile)

    fileConfig(conffile)

    logger = logging.getLogger('psistats2')
    logger.info('Starting psistats2')

    if arguments['ifaces'] == True:
        list_ifaces()
    elif arguments['sensors'] == True:
        list_sensors()
    elif arguments['start'] == True:
        start()
    elif arguments['stop'] == True:
        stop()
    elif arguments['console'] == True:
        console(conf)

