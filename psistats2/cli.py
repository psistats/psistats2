from docopt import docopt
import os
import sys
import logging
from logging.config import fileConfig as logFileConfig
from psistats2 import config
import socket
from psistats2.reporter import Manager
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

PIDFILE = '/var/run/psistats2.pid'


def get_hostname():
  return socket.gethostbyaddr(socket.gethostname())[0]


def print_all_ifaces():

    # TODO: Can this be done using the terminal width instead of hardcoded 80 value?
    print('-' * 80)
    print('List of available network interfaces')
    print(' ')
    print('Use the interface identifier when configuring which interfaces to report')
    print('on.')
    print(' ')

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
    if os.name == 'nt':
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

    if 'hostname' in conf['settings'] and len(conf['settings']['hostname']) > 0:
      hostname = conf['settings']['hostname']
    else:
      hostname = get_hostname()

    logger = logging.getLogger('psistats2')
    logger.info('Starting psistats2')

    manager = Manager(hostname, conf)
    manager.start()

    try:
      manager.join()
    except KeyboardInterrupt:
      manager.stop()


def main():
    run(sys.argv)


def run(argv):
    arguments = docopt(__doc__, argv=argv[1:], version='psistats2 v0.0.1')

    conffile = arguments['--config'] if arguments['--config'] is not None else config.detect_config_file()
    logFileConfig(conffile)

    conf = config.load(conffile)

    if arguments['ifaces'] is True:
        list_ifaces()
    elif arguments['sensors'] is True:
        list_sensors()
    elif arguments['start'] is True:
        start()
    elif arguments['stop'] is True:
        stop()
    elif arguments['console'] is True:
        console(conf)
