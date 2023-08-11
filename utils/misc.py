import re
import sys
import winreg
from pathlib import Path

import requests as requests
import toml
from packaging.version import Version


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


def get_latest_version():
    root_path = Path(getattr(sys, "_MEIPASS", Path(__file__).parents[1]))
    pyproject = toml.load(root_path / "pyproject.toml")

    poetry = pyproject["tool"]["poetry"]
    current_version = poetry["version"]
    github_url = poetry["repository"]
    repository = re.match("(?:https?://)?github.com[:/](.*)", github_url).group(1)

    req = requests.get(url=f"https://api.github.com/repos/{repository}/releases/latest")
    latest_version = req.json().get("tag_tame")
    if not latest_version:
        return

    if Version(latest_version.lstrip("v")) > Version(current_version):
        return f"{github_url}/releases/{latest_version}"
