from windows_toasts import ToastText2, WindowsToaster

import resources
from models import Tunnel


def notify(tunnel: Tunnel, message: str):
    wintoaster = WindowsToaster(resources.APP_TITLE)
    toast = ToastText2()
    toast.SetHeadline(f"{resources.TUNNEL}: {tunnel.name}")
    toast.SetBody(message)
    wintoaster.show_toast(toast)
