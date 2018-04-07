from psireporter import OutputPlugin

class OutputStdout(metaclass=OutputPlugin):
    def send(self, report):
        print(report)


