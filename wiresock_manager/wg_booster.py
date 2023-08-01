import os
from ctypes import *
from ctypes.wintypes import *
from enum import Enum
from pathlib import Path

WG_BOOSTER_PATH = Path(os.environ.get("ProgramFiles"), "WireSock VPN Client", "bin", "wgbooster.dll")
wg_booster_lib = CDLL(WG_BOOSTER_PATH.as_posix())


def logger(m):
    print(m)


class LogLevel(Enum):
    error = 0
    info = 1
    debug = 2
    all = 3


class Stat(Structure):
    _fields_ = [
        ('time_since_last_handshake', c_long),
        ('tx_bytes', c_ulong),
        ('rx_bytes', c_ulong),
        ('estimated_loss', c_float),
        ('estimated_rtt', c_int),
    ]


class WGBooster:
    def __init__(self, log_level: LogLevel = LogLevel.error):
        self._handle = None
        self._log_level = log_level

    @property
    def handle(self) -> HANDLE:
        if not self._handle:
            func_wrapper = CFUNCTYPE(None, c_wchar_p)

            wgb_get_handle = wg_booster_lib.wgb_get_handle
            wgb_get_handle.argtypes = [HANDLE, c_int, c_bool]
            wgb_get_handle.restype = HANDLE
            self._handle = wgb_get_handle(func_wrapper(logger), self.log_level.value, False)
        return self._handle

    def create_tunnel(self, path: str) -> bool:
        wgb_create_tunnel = wg_booster_lib.wgb_create_tunnel_from_file_w
        wgb_create_tunnel.argtypes = [HANDLE, c_wchar_p]
        wgb_create_tunnel.restype = c_bool

        return wgb_create_tunnel(self.handle, path)

    def start_tunnel(self) -> bool:
        wgb_start_tunnel = wg_booster_lib.wgb_start_tunnel
        wgb_start_tunnel.argtypes = [HANDLE]
        wgb_start_tunnel.restype = c_bool

        return wgb_start_tunnel(self.handle)

    def stop_tunnel(self) -> bool:
        wgb_stop_tunnel = wg_booster_lib.wgb_stop_tunnel
        wgb_stop_tunnel.argtypes = [HANDLE]
        wgb_stop_tunnel.restype = c_bool

        return wgb_stop_tunnel(self.handle)

    def drop_tunnel(self) -> bool:
        wgb_drop_tunnel = wg_booster_lib.wgb_drop_tunnel
        wgb_drop_tunnel.argtypes = [HANDLE]
        wgb_drop_tunnel.restype = c_bool

        return wgb_drop_tunnel(self.handle)

    @property
    def log_level(self):
        return self._log_level

    @log_level.setter
    def log_level(self, level: LogLevel):
        wgb_set_log_level = wg_booster_lib.wgb_set_log_level
        wgb_set_log_level.argtypes = [HANDLE, c_int]
        wgb_set_log_level.restype = c_void_p

        wgb_set_log_level(self.handle, level.value)

    @property
    def stat(self) -> Stat:
        wgb_get_tunnel_state = wg_booster_lib.wgb_get_tunnel_state
        wgb_get_tunnel_state.argtypes = [HANDLE]
        wgb_get_tunnel_state.restype = Stat

        return wgb_get_tunnel_state(self.handle)

    @property
    def active(self) -> bool:
        wgb_get_tunnel_active = wg_booster_lib.wgb_get_tunnel_active
        wgb_get_tunnel_active.argtypes = [HANDLE]
        wgb_get_tunnel_active.restype = c_bool

        return wgb_get_tunnel_active(self.handle)
