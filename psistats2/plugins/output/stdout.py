from psistats2.reporter import PsistatsOutputPlugin


class Stdout(PsistatsOutputPlugin):
    PLUGIN_ID = 'stdout'

    def send(self, report):
        print(report)
