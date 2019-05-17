from psistats2.reporter import PsistatsReporterPlugin
import psutil


class Disk(PsistatsReporterPlugin):

    PLUGIN_ID = 'disk'

    def __init__(self, config):
      super(Disk, self).__init__(config)

    def report(self):

        disk_usages = []

        for disk in self.config['disks']:
            usage = psutil.disk_usage(disk)
            disk_usages.append((disk, usage.total, usage.free))

        return disk_usages
