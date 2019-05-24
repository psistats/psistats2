from psistats2.reporter import PsistatsReporterPlugin
import netifaces


class IpAddr(PsistatsReporterPlugin):
    PLUGIN_ID = 'ip_addr'

    def report(self):
        ipaddrs = []

        for iface in self.config['ifaces']:
            try:
              netiface = netifaces.ifaddresses(iface)
              if netifaces.AF_INET in netiface:
                addrs = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
              else:
                addrs = None


              msg = {
                'iface': iface,
                'addrs': addrs
              }

              ipaddrs.append(msg)
            except ValueError:
              self.logger.error('%s is an invalid network interface' % iface)

        return ipaddrs
