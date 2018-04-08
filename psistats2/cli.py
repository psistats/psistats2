from docopt import docopt
import os
import logging
from logging.config import fileConfig
from psistats2 import config
from psistats2.plugins.reporters.network import list_all_ifaces
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
    list_all_ifaces()
    
def list_sensors():
    if os.name is 'nt':
        from psistats2.openhardwaremonitor.openhardwaremonitor import print_all_sensors
    print_all_sensors()
    

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
    
    
    
    
    

