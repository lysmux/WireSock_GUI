import flet

import resources
from models import Tunnel


class TunnelActiveDialog(flet.AlertDialog):
    def __init__(self):
        super(TunnelActiveDialog, self).__init__()
        self.title = flet.Text(value=resources.TUNNEL_ACTIVE_TITLE)
        self.actions = [
            flet.TextButton(resources.CLOSE, on_click=self.close_dlg),
        ]
        self.content = flet.Text(resources.TUNNEL_ACTIVE_CONTENT)

    def close_dlg(self, event: flet.ControlEvent):
        self.open = False
        self.page.update()
