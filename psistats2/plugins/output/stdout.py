from psireporter import OutputPlugin

class OutputStdout(metaclass=OutputPlugin):
    PLUGIN_ID = 'stdout'

    def send(self, report):
        print(report)


