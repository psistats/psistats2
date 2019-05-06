from psistats2.reporter.worker import Report
import platform, calendar
from datetime import datetime
class PsistatsReport(Report):

    def __new__(cls, **kwargs):
        return tuple.__new__(cls, (
            kwargs.get('id', platform.node()),
            kwargs.get('message', None),
            kwargs.get('sender', None),
            calendar.timegm(datetime.utcnow().utctimetuple())
        ))

