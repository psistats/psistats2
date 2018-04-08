from psireporter import ReporterPlugin
import netifaces

def list_all_ifaces():

    addresses = []

    ifaces = netifaces.interfaces()

    for iface in ifaces:
        ifaddrs = netifaces.ifaddresses(iface)

        if netifaces.AF_INET in ifaddrs:

            print("---")
            print("iface: %s" % iface)
            print(ifaddrs[netifaces.AF_INET])


            addresses.append((iface, ifaddrs[netifaces.AF_INET]))

    return addresses


class IPAddrReporter(metaclass=ReporterPlugin):
    PLUGIN_ID = 'ip_addr'

    def report(self):
        ipaddrs = []

        for iface in self.config['ifaces']:
            addrs = netifaces.ifaddresses(iface)[netifaces.AF_LINK]

            ipaddrs.append(addrs)

        return ipaddrs

