import flet

import resources
from models import Tunnel


class TunnelErrorDialog(flet.AlertDialog):
    def __init__(self, tunnel: Tunnel):
        super(TunnelErrorDialog, self).__init__()
        self.title = flet.Text(value=resources.TUNNEL_START_ERROR_TITLE)
        self.actions = [
            flet.ElevatedButton(text=resources.EDIT_TUNNEL, on_click=self.go_edit),
            flet.TextButton(resources.CLOSE, on_click=self.close_dlg),
        ]
        self.content = flet.Text(resources.TUNNEL_START_ERROR_CONTENT)

        self.tunnel = tunnel

    def go_edit(self, event: flet.ControlEvent):
        self.page.go(f"/edit/{self.tunnel.name}")

    def close_dlg(self, event: flet.ControlEvent):
        self.open = False
        self.page.update()
