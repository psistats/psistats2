from psistats2.reporter import PsistatsReporterPlugin
import psutil


class Mem(PsistatsReporterPlugin):

    PLUGIN_ID = 'mem'

    def report(self):
        mem = psutil.virtual_memory()
        return (mem.total, mem.free)
