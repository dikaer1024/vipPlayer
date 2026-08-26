import os
import uuid
import hashlib
import platform


class MachineUtil:
    PRODUCT = "vipPlayer"

    @staticmethod
    def get_machine_code(product):
        disk = MachineUtil.get_disk_serial()
        cpu = MachineUtil.get_cpu_id()
        mem = MachineUtil.get_memory_gb()

        return f"{product}-{disk}-{cpu}-{mem}";
        #return hashlib.md5(raw.encode("utf-8")).hexdigest().upper()

    @staticmethod
    def get_disk_serial():
        try:
            path = os.path.abspath(os.sep)
            return hashlib.md5(path.encode()).hexdigest()[:8].upper()
        except:
            return "UNKNOWN"

    @staticmethod
    def get_cpu_id():
        try:
            cpu = platform.processor()
            if not cpu:
                cpu = str(uuid.getnode())
            return hashlib.md5(cpu.encode()).hexdigest()[:8].upper()
        except:
            return "UNKNOWN"

    @staticmethod
    def get_memory_gb():
        try:
            if os.name == "nt":
                import ctypes
                kernel32 = ctypes.windll.kernel32
                c_ulonglong = ctypes.c_ulonglong
                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", c_ulonglong),
                        ("ullAvailPhys", c_ulonglong),
                        ("ullTotalPageFile", c_ulonglong),
                        ("ullAvailPageFile", c_ulonglong),
                        ("ullTotalVirtual", c_ulonglong),
                        ("ullAvailVirtual", c_ulonglong),
                        ("ullAvailExtendedVirtual", c_ulonglong),
                    ]
                stat = MEMORYSTATUSEX()
                stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
                return f"{stat.ullTotalPhys // (1024**3)}G"
        except:
            pass
        return "0G"