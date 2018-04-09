import servicemanager
import socket
import sys
import win32event
import win32service
import win32serviceutil
import time

class PsistatsService(win32serviceutil.ServiceFramework):
    _svc_name = 'Psistats2'
    _svc_display_name = 'Psistats2 Monitoring Tool'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)

        self.evt_stop = win32event.CreateEvent(None, 0, 0, None)
        self.need_to_stop = False

        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.evt_stop)
        self.need_to_stop = True

    def SvcDoRun(self):

        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name, '')
        )

        self.main()

    def main(self):

        while True:
            if self.need_to_stop is True:
                break
            time.sleep(5)

