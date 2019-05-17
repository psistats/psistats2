from psistats2.reporter import PsistatsOutputPlugin


class Logging(PsistatsOutputPlugin):

    PLUGIN_ID = 'logging'

    def send(self, report):
      self.logger.info('[%s:%s] - %s' % (report['hostname'], report['sender'], report['message']))
