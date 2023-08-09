import flet

import resources
from models import Tunnel
from utils.config_manager import save_config


class TunnelCreateDialog(flet.AlertDialog):
    def __init__(self):
        super().__init__()
        self.title = flet.Text(value=resources.TUNNEL_CREATE_TITLE)
        self.actions = [
            flet.TextButton(resources.CREATE, on_click=self.create_tunnel),
            flet.TextButton(resources.CLOSE, on_click=self.close_dlg),
        ]
        self.content = flet.TextField(label=resources.ENTER_TUNNEL_NAME)

    def create_tunnel(self, event: flet.ControlEvent):
        tunnel_name = self.content.value
        tunnel = Tunnel(name=tunnel_name)
        save_config(tunnel)

        self.page.go(f"/edit/{tunnel_name}")

    def close_dlg(self, event: flet.ControlEvent):
        self.open = False
        self.page.update()
