import ctypes
import struct

def uptime3():
    libc = ctypes.CDLL('libc.so.6')
    buf = ctypes.create_string_buffer(4096)

    if libc.sysinfo(buf) != 0:
        print('failed')
        return -1

    uptime = struct.unpack_from('@l', buf.raw)[0]
    return uptime

print('Uptime: %s' % uptime3())
