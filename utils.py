import sys
from os import getenv
from pathlib import Path


def get_appdata_dir(*paths):
    if sys.platform.startswith("win"):
        os_path = getenv("LOCALAPPDATA")
    elif sys.platform.startswith("darwin"):
        os_path = "~/Library/Application Support"
    else:
        os_path = getenv("XDG_DATA_HOME", "~/.local/share")

    path = Path(os_path, "WireSock", *paths)
    path.mkdir(parents=True, exist_ok=True)

    return path.expanduser()
