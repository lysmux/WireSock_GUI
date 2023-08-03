import flet

from models import Tunnel


class TunnelErrorDialog(flet.AlertDialog):
    def __init__(self, tunnel: Tunnel):
        super(TunnelErrorDialog, self).__init__()
        self.title = flet.Text(value="Tunnel start error")
        self.actions = [
            flet.ElevatedButton(text="Edit tunnel", on_click=self.go_edit),
            flet.TextButton("Close", on_click=self.close_dlg),
        ]
        self.content = flet.Text("An error occurred during the tunnel startup")

        self.tunnel = tunnel

    def go_edit(self, event: flet.ControlEvent):
        self.page.go(f"/edit/{self.tunnel.name}")

    def close_dlg(self, event: flet.ControlEvent):
        self.open = False
        self.page.update()
