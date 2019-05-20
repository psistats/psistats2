import paho.mqtt.client as mqtt
import json
from psistats2.reporter import PsistatsOutputPlugin


class Mqtt(PsistatsOutputPlugin):

    PLUGIN_ID = 'mqtt'

    def __init__(self, config):
      super(Mqtt, self).__init__(config)
      self._client = mqtt.Client()
      self.initialized = False

    def init(self):

        if self.config['username'] and self.config['password']:
            self._client.username_pw_set(self.config['username'], self.config['password'])

        if self.config['ssl'] != 'no':
            self._client.tls_set()

        self._client.connect(self.config['host'], int(self.config['port']), int(self.config['timeout']))
        self.logger.info('Connected to MQTT Broker')
        self.initialized = True

    def send(self, report):
        if self.initialized is False:
            self.init()

        self._client.publish("psistats2/%s" % report.hostname, json.dumps(dict(report)))
