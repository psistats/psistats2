import paho.mqtt.client as mqtt
import json
from psistats2.reporter import PsistatsOutputPlugin


class Mqtt(PsistatsOutputPlugin):

    PLUGIN_ID = 'mqtt'

    def __init__(self, config):
      super(Mqtt, self).__init__(config)
      self.initialized = False

    def init(self):

        self._client = mqtt.Client()

        if self.config['username'] and self.config['password']:
            self._client.username_pw_set(self.config['username'], self.config['password'])

        if self.config['ssl'] != 'no':
            self._client.tls_set()

        try:
          self._client.connect(self.config['host'], int(self.config['port']), int(self.config['timeout']))
          self.logger.info('MQTT Client initialized')
          self.initialized = True
        except Exception as e:
          self.logger.error('Error connceting to MQTT: %s' % e)

    def send(self, report):
        if self.initialized is False:
            self.init()
        if self.initialized is False:
          return

        if self.config['topic_per_sender']:
            topic = "psistats2/%s/%s" % (report['hostname'], report['sender'])
        else:
            topic = "psistats2/%s" % report['hostname']

        res = self._client.publish(topic, json.dumps(dict(report)))

        if (res[0] != 0):
          self.initialized = False

        self._client.loop()
