import psutil
from psistats2.reporter.plugin import PsistatsReporterPlugin


class CpuPerCore(PsistatsReporterPlugin):

  PLUGIN_ID = 'cpu_per_core'

  def __init__(self, config):
    super().__init__(config)

  def report(self, config=None):
      return psutil.cpu_percent(percpu=True)


class CpuTotal(PsistatsReporterPlugin):

    PLUGIN_ID = 'cpu_total'

    def report(self, config=None):
        return psutil.cpu_percent(percpu=False)
