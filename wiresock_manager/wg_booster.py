import ctypes
import winreg
from ctypes.wintypes import HANDLE
from enum import IntEnum
from pathlib import Path

ws_location_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\NTKernelResources\\WinpkFilterForVPNClient")
ws_location = winreg.QueryValueEx(ws_location_key, "InstallLocation")[0]
wg_booster_path = Path(ws_location, "bin", "wgbooster.dll")
wg_booster_lib = ctypes.CDLL(wg_booster_path.as_posix())


class LogLevel(IntEnum):
    error = 0
    info = 1
    debug = 2
    all = 3

    def __init__(self, value):
        self._as_parameter = int(value)

    @classmethod
    def from_param(cls, obj):
        return int(obj)


class WgStats(ctypes.Structure):
    _fields_ = [
        ("latest_handshake", ctypes.c_int64),
        ("tx_bytes", ctypes.c_uint64),
        ("rx_bytes", ctypes.c_uint64),
        ("estimated_loss", ctypes.c_float),
        ("estimated_rtt", ctypes.c_int32),
    ]


class WGBooster:
    def __init__(self, va_mode: bool = False):
        self.va_mode = va_mode

    def get_handle(self, log_func, log_level: LogLevel) -> HANDLE:
        func_wrapper = ctypes.CFUNCTYPE(None, ctypes.POINTER(ctypes.c_wchar_p))

        if self.va_mode:
            wgb_get_handle = wg_booster_lib.wgbp_get_handle
        else:
            wgb_get_handle = wg_booster_lib.wgb_get_handle
        wgb_get_handle.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_bool]
        wgb_get_handle.restype = HANDLE
        return wgb_get_handle(func_wrapper(log_func), 0, False)

    def create_tunnel(self, handle: HANDLE, path: str) -> bool:
        if self.va_mode:
            wgb_create_tunnel = wg_booster_lib.wgbp_create_tunnel_from_file_w
        else:
            wgb_create_tunnel = wg_booster_lib.wgb_create_tunnel_from_file_w
        wgb_create_tunnel.argtypes = [HANDLE, ctypes.c_wchar_p]
        wgb_create_tunnel.restype = ctypes.c_bool

        return wgb_create_tunnel(handle, path)

    def start_tunnel(self, handle: HANDLE) -> bool:
        if self.va_mode:
            wgb_start_tunnel = wg_booster_lib.wgbp_start_tunnel
        else:
            wgb_start_tunnel = wg_booster_lib.wgb_start_tunnel
        wgb_start_tunnel.argtypes = [HANDLE]
        wgb_start_tunnel.restype = ctypes.c_bool

        return wgb_start_tunnel(handle)

    def stop_tunnel(self, handle: HANDLE) -> bool:
        if self.va_mode:
            wgb_stop_tunnel = wg_booster_lib.wgbp_stop_tunnel
        else:
            wgb_stop_tunnel = wg_booster_lib.wgb_stop_tunnel
        wgb_stop_tunnel.argtypes = [HANDLE]
        wgb_stop_tunnel.restype = ctypes.c_bool

        return wgb_stop_tunnel(handle)

    def drop_tunnel(self, handle: HANDLE) -> bool:
        if self.va_mode:
            wgb_drop_tunnel = wg_booster_lib.wgbp_drop_tunnel
        else:
            wgb_drop_tunnel = wg_booster_lib.wgb_drop_tunnel
        wgb_drop_tunnel.argtypes = [HANDLE]
        wgb_drop_tunnel.restype = ctypes.c_bool

        return wgb_drop_tunnel(handle)

    def get_stat(self, handle: HANDLE) -> WgStats:
        if self.va_mode:
            wgb_get_tunnel_state = wg_booster_lib.wgbp_get_tunnel_state
        else:
            wgb_get_tunnel_state = wg_booster_lib.wgb_get_tunnel_state
        wgb_get_tunnel_state.argtypes = [HANDLE]
        wgb_get_tunnel_state.restype = WgStats

        return wgb_get_tunnel_state(handle)

    def is_active(self, handle: HANDLE) -> bool:
        if self.va_mode:
            wgb_get_tunnel_active = wg_booster_lib.wgbp_get_tunnel_active
        else:
            wgb_get_tunnel_active = wg_booster_lib.wgb_get_tunnel_active
        wgb_get_tunnel_active.argtypes = [HANDLE]
        wgb_get_tunnel_active.restype = ctypes.c_bool

        return wgb_get_tunnel_active(handle)

    def set_log_level(self, handle: HANDLE, level: LogLevel):
        if self.va_mode:
            wgb_set_log_level = wg_booster_lib.wgbp_set_log_level
        else:
            wgb_set_log_level = wg_booster_lib.wgb_set_log_level
        wgb_set_log_level.argtypes = [HANDLE, ctypes.c_int]
        wgb_set_log_level.restype = ctypes.c_void_p

        wgb_set_log_level(handle, level.value)
