import flet

import resources
from dialogs.tunnel_error import TunnelErrorDialog
from models import Tunnel
from utils.notify import notify
from wiresock_manager.wiresock_manager import WSManager


def change_tunnel_state(page: flet.Page, tunnel: Tunnel, connect: bool):
    if connect:
        if not WSManager().connect_tunnel(tunnel):
            dlg = TunnelErrorDialog(tunnel)
            dlg.open = True
            page.dialog = dlg
            page.update()
            return False
        else:
            notify(tunnel=tunnel, message=resources.CONNECT_NOTIFY)
    else:
        WSManager().disconnect_tunnel()
        notify(tunnel=tunnel, message=resources.DISCONNECT_NOTIFY)
    return True
