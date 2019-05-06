

from docopt import docopt
import os, sys

print('System path: %s' % sys.path)
# print('Env path: %s' % os.environ['PYTHONPATH'].split(os.pathsep))

import logging
from logging.config import fileConfig
from psistats2 import config
from psistats2.report import PsistatsReport
import time
from psistats2.reporter import Manager
from psistats2.plugins.output import *
from psistats2.plugins.reporters import *
import ifaddr

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

PIDFILE='/var/run/psistats2.pid'

       

def print_all_ifaces():

    # TODO: Can this be done using the terminal width instead of hardcoded 80 value?
    print('-' * 80)
    print('List of available network interfaces')
    print(' ')
    print('Use the interface identifier when configuring which interfaces to report')
    print('on.')
    print(' ')

    addresses = []

    ipaddrs = []
    for adapter in ifaddr.get_adapters():
        ipaddrs.append((adapter.name, adapter.nice_name, [ip.ip for ip in adapter.ips]))

    namewidth = max([len(name) for name, nice_name, ips in ipaddrs]) + 2
    nicenamewidth = max([len(nice_name) for name, nice_name, ips in ipaddrs]) + 2

    if namewidth < 12:
        namewidth = namewidth + (12 - namewidth)

    if nicenamewidth < 12:
        nicenamewidth = nicenamewidth + (12 - nicenamewidth)

    sys.stdout.write('Identifier'.ljust(namewidth))
    sys.stdout.write('Nice Name'.ljust(nicenamewidth))
    sys.stdout.write('IPs')
    sys.stdout.write(os.linesep)
    sys.stdout.write('-' * 80)
    sys.stdout.write(os.linesep)

    for name, nice_name, ips in ipaddrs:

        first_ip = ips[0]
        if type(first_ip) is tuple:
            first_ip = ips[0][0]
        
        try:
            first_ip = first_ip.decode('utf-8')
        except AttributeError:
            pass
            
        try:
            name = name.decode('utf-8')
        except AttributeError:
            pass
        
        try:
            nice_name = name.decode('utf-8')
        except AttributeError:
            pass
	
        sys.stdout.write('%s' % (name.ljust(namewidth)))
        sys.stdout.write('%s' % (nice_name.ljust(nicenamewidth)))
        sys.stdout.write('%s' % first_ip)
        sys.stdout.write(os.linesep)

        if len(ips) > 1:
            for ip in ips[1:]:
                
                if type(ip) is tuple:
                    ip = ip[0]
           
                try:
                    ip = ip.decode('utf-8')
                except AttributeError:
                    pass
            
                sys.stdout.write(' ' * (namewidth + nicenamewidth))
                sys.stdout.write(ip)
                sys.stdout.write(os.linesep)




def list_ifaces():
    print_all_ifaces()

def list_sensors():
    if os.name is 'nt':
        from psistats2.openhardwaremonitor.openhardwaremonitor import print_all_sensors
    else:
        from psistats2.libsensors.libsensors import print_all_sensors
    print_all_sensors()

def start():
    pass
    
def stop():
    pass


def restart():
    stop()
    start()

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

def main():
    run(sys.argv)


def run(argv):



    arguments = docopt(__doc__, argv=argv[1:], version='psistats2 v0.0.1')

    conffile = arguments['--config'] if arguments['--config'] is not None else config.detect_config_file()

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

