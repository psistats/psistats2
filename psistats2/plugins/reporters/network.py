from psireporter import ReporterPlugin
import ifaddr
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

        for adapter in ifaddr.get_adapters():
            ipaddrs.append((adapter.name, [ip.ip for ip in adapter.ips]))

        return ipaddrs

