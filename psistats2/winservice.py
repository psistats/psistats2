import servicemanager
import socket
import sys, os
import win32event
import win32service
import win32serviceutil
import time
import logging
import io
import traceback
from psistats2 import config
from psistats2.report import PsistatsReport
from psistats2.psireporter import Manager
from logging.config import fileConfig

class PsistatsService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'Psistats2'
    _svc_display_name_ = 'Psistats2 Monitoring Tool'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)

        self.evt_stop = win32event.CreateEvent(None, 0, 0, None)
        self.need_to_stop = False

        socket.setdefaulttimeout(60)

    def SvcStop(self):
        servicemanager.LogInfoMsg('Stopping service')
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.evt_stop)
        self.need_to_stop = True

    def SvcDoRun(self):

        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, '')
        )

        try:
            self.main()
        except Exception as e:
            output = io.StringIO()
            
            traceback.print_tb(e.__traceback__, file=output)

            servicemanager.LogErrorMsg('ERROR: %s' % e)
            servicemanager.LogErrorMsg('ERROR: %s' % output.getvalue())
            
            output.close()

    def main(self):

        home_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
    
        # home_dir = 'c:\\Users\\IEUser'
    
        servicemanager.LogInfoMsg('HOME DIR: %s' % home_dir)
    
        conffile = os.path.join(home_dir, 'psistats.conf')
        
        if os.path.exists(conffile) == False:
            raise Exception("%s does not exist" % conffile)
        
        conf = config.load(conffile)
        fileConfig(conffile)
        
        logger = logging.getLogger('psistats2')
        logger.info('Starting psistats2')
    
        servicemanager.LogInfoMsg('Starting Manager thread')
        
        manager = Manager(conf, reportClass=PsistatsReport)
        manager.start()
        
        while True:
            if self.need_to_stop is True:
                break
            time.sleep(5)
        
        servicemanager.LogInfoMsg('Stopping Manager thread')
        manager.stop()
    
        servicemanager.LogInfoMsg('Done')
