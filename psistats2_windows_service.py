from psistats2.plugins.reporters.cpu import CpuPerCore, CpuTotal
from psistats2.plugins.reporters.mem import MemoryReport
from psistats2.plugins.reporters.disk import DiskUsage
from psistats2.plugins.reporters.sensors import LmSensors
from psistats2.plugins.reporters.uptime import UptimeReporter
from psistats2.plugins.reporters.network import IPAddrReporter
from psistats2.plugins.output.stdout import OutputStdout
from psistats2.plugins.output.logging import OutputLogging
from psistats2.plugins.output.amqp import AMQPOutput
from psistats2.plugins.output.http import HttpOutput
from psistats2 import config
from psistats2.cli import main

from psistats2.winservice import PsistatsService

import servicemanager
import win32serviceutil

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(PsistatsService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(PsistatsService)