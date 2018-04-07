import psutil
from psireporter.plugin import ReporterPlugin

class CpuPerCore(metaclass=ReporterPlugin):

    PLUGIN_ID = 'cpu_per_core'

    def report(self, config=None):
        return psutil.cpu_percent(percpu=True)


class CpuTotal(metaclass=ReporterPlugin):

    PLUGIN_ID = 'cpu_total'

    def report(self, config=None):
        return psutil.cpu_percent(percpu=False)

