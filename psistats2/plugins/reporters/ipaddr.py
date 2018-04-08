from psireporter import ReporterPlugin
import netifaces

class IPAddrReporter(metaclass=ReporterPlugin):
    PLUGIN_ID = 'ip_addr'
    
    def report(self):
        ipaddrs = []
        
        for iface in self.config['ifaces']:
            addrs = netifaces.ifaddresses(iface)[netifaces.AF_LINK]
        
            ipaddrs.append(addrs)
        
        return ipaddrs
            