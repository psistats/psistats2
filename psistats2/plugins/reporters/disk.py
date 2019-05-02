from psistats2.psireporter import ReporterPlugin
import psutil

class DiskUsage(metaclass=ReporterPlugin):

    PLUGIN_ID = 'disk_usage'

    def report(self):

        disk_usages = []

        for disk in self.config['disks']:
            usage = psutil.disk_usage(disk)
            disk_usages.append((disk, usage.total, usage.free))

        return disk_usages
