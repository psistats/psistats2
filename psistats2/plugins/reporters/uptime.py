from uptime import uptime
from psireporter import ReporterPlugin

class UptimeReporter(metaclass=ReporterPlugin):

    PLUGIN_ID='uptime'

    def report(self):
        return uptime()
        
