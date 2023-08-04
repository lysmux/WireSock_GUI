from logging import Handler

import flet
from windows_toasts import WindowsToaster, ToastText2

import resources
from dialogs.tunnel_error import TunnelErrorDialog
from models import Tunnel
from wiresock_manager.wiresock_manager import WSManager


class LogHandler(Handler):
    def __init__(self):
        super(LogHandler, self).__init__()
        self.log_function = None

    def emit(self, record):
        message = self.format(record)

        if self.log_function:
            self.log_function(message)


def notify(tunnel_name: str, message: str):
    wintoaster = WindowsToaster(resources.APP_TITLE)
    toast = ToastText2()
    toast.SetHeadline(f"{resources.TUNNEL}: {tunnel_name}")
    toast.SetBody(message)
    wintoaster.show_toast(toast)


def change_tunnel_state(page: flet.Page, tunnel: Tunnel, connect: bool):
    if connect:
        if not WSManager().connect_tunnel(tunnel):
            dlg = TunnelErrorDialog(tunnel)
            dlg.open = True
            page.dialog = dlg
            page.update()
            return False
        else:
            notify(tunnel_name=tunnel.name, message=resources.CONNECT_NOTIFY)
    else:
        WSManager().disconnect_tunnel()
        notify(tunnel_name=tunnel.name, message=resources.DISCONNECT_NOTIFY)
    return True
