import ctypes
import logging
import winreg
from ctypes.wintypes import HANDLE
from enum import IntEnum
from pathlib import Path

ws_location_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\NTKernelResources\\WinpkFilterForVPNClient")
ws_location = winreg.QueryValueEx(ws_location_key, "InstallLocation")[0]
wg_booster_path = Path(ws_location, "bin", "wgbooster.dll")
wg_booster_lib = ctypes.CDLL(wg_booster_path.as_posix())

logger = logging.getLogger("wire_sock")
logger.setLevel(logging.INFO)


class LogLevel(IntEnum):
    error = 0
    info = 1
    debug = 2
    all = 3

    def __init__(self, value):
        self._as_parameter = int(value)

    # Option 2: define the class method `from_param`.
    @classmethod
    def from_param(cls, obj):
        return int(obj)


class Stat(ctypes.Structure):
    _fields_ = [
        ('time_since_last_handshake', ctypes.c_long),
        ('tx_bytes', ctypes.c_ulong),
        ('rx_bytes', ctypes.c_ulong),
        ('estimated_loss', ctypes.c_float),
        ('estimated_rtt', ctypes.c_int),
    ]


class WGBooster:
    def __init__(self, va_mode: bool = False, log_level: LogLevel = LogLevel.all):
        self._handle = None
        self.log_level = log_level
        self.va_mode = va_mode

    @property
    def handle(self) -> HANDLE:
        if not self._handle:
            func_wrapper = ctypes.CFUNCTYPE(None, ctypes.POINTER(ctypes.c_wchar_p))

            if self.va_mode:
                wgb_get_handle = wg_booster_lib.wgbp_get_handle
            else:
                wgb_get_handle = wg_booster_lib.wgb_get_handle
            wgb_get_handle.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_bool]
            wgb_get_handle.restype = HANDLE
            self._handle = wgb_get_handle(func_wrapper(lambda msg: logger.info(msg)), 0, False)
        return self._handle

    def create_tunnel(self, path: str) -> bool:
        if self.va_mode:
            wgb_create_tunnel = wg_booster_lib.wgbp_create_tunnel_from_file_w
        else:
            wgb_create_tunnel = wg_booster_lib.wgb_create_tunnel_from_file_w
        wgb_create_tunnel.argtypes = [HANDLE, ctypes.c_wchar_p]
        wgb_create_tunnel.restype = ctypes.c_bool

        return wgb_create_tunnel(self.handle, path)

    def start_tunnel(self) -> bool:
        if self.va_mode:
            wgb_start_tunnel = wg_booster_lib.wgbp_start_tunnel
        else:
            wgb_start_tunnel = wg_booster_lib.wgb_start_tunnel
        wgb_start_tunnel.argtypes = [HANDLE]
        wgb_start_tunnel.restype = ctypes.c_bool

        return wgb_start_tunnel(self.handle)

    def stop_tunnel(self):
        if self.va_mode:
            wgb_stop_tunnel = wg_booster_lib.wgbp_stop_tunnel
        else:
            wgb_stop_tunnel = wg_booster_lib.wgb_stop_tunnel
        wgb_stop_tunnel.argtypes = [HANDLE]
        wgb_stop_tunnel.restype = ctypes.c_bool

        wgb_stop_tunnel(self.handle)

    def drop_tunnel(self):
        if self.va_mode:
            wgb_drop_tunnel = wg_booster_lib.wgbp_drop_tunnel
        else:
            wgb_drop_tunnel = wg_booster_lib.wgb_drop_tunnel
        wgb_drop_tunnel.argtypes = [HANDLE]
        wgb_drop_tunnel.restype = ctypes.c_bool

        wgb_drop_tunnel(self.handle)
        self._handle = None

    def get_stat(self) -> Stat:
        if self.va_mode:
            wgb_get_tunnel_state = wg_booster_lib.wgbp_get_tunnel_state
        else:
            wgb_get_tunnel_state = wg_booster_lib.wgb_get_tunnel_state
        wgb_get_tunnel_state.argtypes = [HANDLE]
        wgb_get_tunnel_state.restype = Stat

        return wgb_get_tunnel_state(self.handle)

    def is_active(self) -> bool:
        if self.va_mode:
            wgb_get_tunnel_active = wg_booster_lib.wgbp_get_tunnel_active
        else:
            wgb_get_tunnel_active = wg_booster_lib.wgb_get_tunnel_active
        wgb_get_tunnel_active.argtypes = [HANDLE]
        wgb_get_tunnel_active.restype = ctypes.c_bool

        return wgb_get_tunnel_active(self.handle)

    def set_log_level(self, level: LogLevel):
        if self.va_mode:
            wgb_set_log_level = wg_booster_lib.wgbp_set_log_level
        else:
            wgb_set_log_level = wg_booster_lib.wgb_set_log_level
        wgb_set_log_level.argtypes = [HANDLE, ctypes.c_int]
        wgb_set_log_level.restype = ctypes.c_void_p

        wgb_set_log_level(self.handle, level.value)
        self.log_level = level
