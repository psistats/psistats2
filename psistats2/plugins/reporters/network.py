from psireporter import ReporterPlugin
import ifaddr
import sys, os

def print_all_ifaces():

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
        sys.stdout.write(name.ljust(namewidth))
        sys.stdout.write(nice_name.ljust(nicenamewidth))
        sys.stdout.write(ips[0])
        sys.stdout.write(os.linesep)

        if len(ips) > 1:
            for ip in ips[1:]:
                sys.stdout.write(' ' * (namewidth + nicenamewidth))
                sys.stdout.write(ip[0])
                sys.stdout.write(os.linesep)


class IPAddrReporter(metaclass=ReporterPlugin):
    PLUGIN_ID = 'ip_addr'

    def report(self):
        ipaddrs = []

        for adapter in ifaddr.get_adapters():
            ipaddrs.append((adapter.name, [ip.ip for ip in adapter.ips]))

        return ipaddrs

