from psistats2.reporter import OutputPlugin
import time, logging, json, socket

class UDPOutput(metaclass=OutputPlugin):

    PLUGIN_ID = 'udp'

    def __init__(self):
        self.logger = logging.getLogger('psistats.udp')

    def send(self, report):
        self.logger.debug('send udp packet')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(bytes(json.dumps(dict(report)), 'utf-8'), (self.config['host'], int(self.config['port'])))


