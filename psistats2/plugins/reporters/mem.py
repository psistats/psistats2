from psistats2.psireporter import ReporterPlugin
import psutil

class MemoryReport(metaclass=ReporterPlugin):

    PLUGIN_ID = 'memory'

    def report(self):
        mem = psutil.virtual_memory()
        return (mem.total, mem.free)


