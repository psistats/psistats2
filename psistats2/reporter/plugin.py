import logging


class PsistatsPlugin():
  PLUGIN_ID = ""
  PLUGIN_TYPE = ""

  def __init__(self, config):
    self.config = config

    if len(self.PLUGIN_ID) == 0:
      raise RuntimeError("Plugin id not set")

    if len(self.PLUGIN_TYPE) == 0:
      raise RuntimeError("Plugin type is not set")

    self.logger = logging.getLogger('psistats.%s' % self.PLUGIN_ID)


class PsistatsOutputPlugin(PsistatsPlugin):
  PLUGIN_TYPE = "output"

  def __init__(self, config):
    super().__init__(config)

  def init(self):
    pass

  def send(self, report):
    pass


class PsistatsReporterPlugin(PsistatsPlugin):
  PLUGIN_TYPE = "reporter"

  def __init__(self, config):
    super().__init__(config)

  def init(self):
    pass

  def report(self):
    pass
