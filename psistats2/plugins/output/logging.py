from psireporter import OutputPlugin
import logging

class OutputLogging(metaclass=OutputPlugin):

    PLUGIN_ID = 'logging'

    def __init__(self):
        self.logger = logging.getLogger('psistats2')

    def send(self, report):
        self.logger.info('[%s] - %s' % (report.sender, report.message))

