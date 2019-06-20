from psistats2.reporter import PsistatsOutputPlugin
import time
import json


class Amqp(PsistatsOutputPlugin):

    PLUGIN_ID = 'amqp'

    def __init__(self, config):
      super(Amqp, self).__init__(config)

      self._connection = None
      self._channel = None
      self.initialized = False

    def init(self):

        try:
            import pika
        except ImportError:
            self.logger.error('Pika library is missing')
            return

        credentials = pika.credentials.PlainCredentials(
            username=self.config['username'],
            password=self.config['password'],
            erase_on_connect=True
        )

        params = pika.connection.ConnectionParameters(
            host=self.config['host'],
            port=int(self.config['port']),
            virtual_host=self.config['vhost'],
            credentials=credentials)

        self._connection = pika.BlockingConnection(params)
        self._channel = self._connection.channel()
        self.initialized = True

    def send(self, report):
        if self.initialized is False:
            self.init()
            if self.initialized is False:
                self.logger.error('Failed to initialize!')
                time.sleep(10)
                return

        self._channel.basic_publish(
            self.config['exchange'], 
            'psistats2.%s.%s' % (report['hostname'], report['sender']), 
            json.dumps(dict(report)))
