from psistats2.reporter import PsistatsReporterPlugin
import ctypes
import struct
import os


class Uptime(PsistatsReporterPlugin):

    PLUGIN_ID = 'uptime'

    def __init__(self, config):
      super(Uptime, self).__init__(config)

      if os.name == 'posix':
          self._lib = ctypes.CDLL('libc.so.6')
          self._buf = ctypes.create_string_buffer(4096)
      elif os.name == 'nt':
          self._lib = ctypes.windll.kernel32
          self._lib.GetTickCount64.restype = ctypes.c_uint64
      else:
          self._lib = None

    def _nt(self):
        """Get uptime for windows"""
        return self._lib.GetTickCount64() / 1000.

    def _posix(self):
        """Get uptime from posix systems"""
        if self._lib.sysinfo(self._buf) == 0:
            return struct.unpack_from('@l', self._buf.raw)[0]
        return -1

    def report(self):

        if os.name == 'posix':
            return self._posix()
        elif os.name == 'nt':
            return self._nt()
        else:
            return -1
