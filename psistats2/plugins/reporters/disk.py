from psireporter import ReporterPlugin
import psutil

class DiskUsage(metaclass=ReporterPlugin):

    PLUGIN_ID = 'disk_usage'

    def report(self):

        disk_usages = []

        print('config:', self.config)

        for disk in self.config['disks']:
            usage = psutil.disk_usage(disk)
            disk_usages.append((disk, usage.total, usage.used))

        return disk_usages
