from psistats2.reporter import PsistatsReporterPlugin
import netifaces


class IpAddr(PsistatsReporterPlugin):
    PLUGIN_ID = 'ip_addr'

    def report(self):
        ipaddrs = []

        for iface in self.config['ifaces']:
            try:
              addrs = netifaces.ifaddresses(iface)[netifaces.AF_LINK]
              ipaddrs.append(addrs)
            except ValueError:
              self.logger.error('%s is an invalid network interface' % iface)

        return ipaddrs
