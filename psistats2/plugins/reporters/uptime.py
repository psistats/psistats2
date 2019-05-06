from psistats2.reporter import ReporterPlugin
import ctypes
import struct
import os

class UptimeReporter(metaclass=ReporterPlugin):

    PLUGIN_ID='uptime'

    def __init__(self):

        print('??? %s' % os.name)

        if os.name is 'posix':
            self._lib = ctypes.CDLL('libc.so.6')
            self._buf = ctypes.create_string_buffer(4096)
        elif os.name is 'nt':
            self._lib = ctypes.windll.kernel32
            self._lib = ctypes.c_uint64
        else:
            self._lib = None


    def _nt(self):
        """Get uptime for windows"""
        return self._lib.GetTickCount64() / 1000.
        
    def _posix(self):
        """Get uptime from posix systems"""
        if self._lib.sysinfo(self._buf) is 0:
            return struct.unpack_from('@l', self._buf.raw)[0]
        return -1

    def report(self):

        if os.name is 'posix':
            return self._posix()
        elif os.name is 'nt':
            return self._nt()
        else:
            return -1
        
