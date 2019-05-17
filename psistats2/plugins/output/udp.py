from psistats2.reporter import PsistatsOutputPlugin
import json
import socket


class Udp(PsistatsOutputPlugin):

    PLUGIN_ID = 'udp'

    def send(self, report):
        self.logger.debug('send udp packet')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(bytes(json.dumps(dict(report)), 'utf-8'), (self.config['host'], int(self.config['port'])))