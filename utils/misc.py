import winreg
from pathlib import Path


def get_wiresock_bin() -> Path | None:
    try:
        location_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\NTKernelResources\\WinpkFilterForVPNClient")
        location = winreg.QueryValueEx(location_key, "InstallLocation")[0]
    except FileNotFoundError:
        return

    bin_path = Path(location, "bin")
    if not bin_path.exists():
        return
    return bin_path
