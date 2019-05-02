from psistats2.psireporter import OutputPlugin
import time, logging, json

class AMQPOutput(metaclass=OutputPlugin):

    PLUGIN_ID = 'amqp'

    def __init__(self):
        self._connection = None
        self._channel = None
        self.initialized = False
        self.logger = logging.getLogger('psistats.amqp')

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
        self._channel.exchange_declare(
            exchange=self.config['exchange'],
            exchange_type='topic',
            durable=False,
            auto_delete=False
        )

        self.initialized = True

    def send(self, report):
        if self.initialized is False:
            self.init()
            if self.initialized is False:
                self.logger.error('Failed to initialize!')
                time.sleep(10)
                return

        self._channel.basic_publish(self.config['exchange'], 'psistats.' + report.id, json.dumps(dict(report)))

