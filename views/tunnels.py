import pathlib

import flet

import wiresock_manager
from models import Tunnel


class TunnelsView(flet.UserControl):
    def __init__(self):
        super().__init__()
        self.expand = True

        self.info_column = flet.Column()
        self.file_picker = flet.FilePicker(on_result=self.on_tunnel_add)

        self.tunnels = [wiresock_manager.load_config(pathlib.Path("conf")),
                        wiresock_manager.load_config(pathlib.Path("pc.conf"))]

    def build(self):
        tunnels_view = flet.Column(scroll=flet.ScrollMode.AUTO, expand=True)

        for tunnel in self.tunnels:
            tunnels_view.controls.append(
                flet.TextButton(text=tunnel.name, on_click=self.on_tunnel_click, data=tunnel)
            )

        return flet.Row([
            flet.Column([
                tunnels_view,
                self.file_picker,
                flet.ElevatedButton(text="Add tunnel",
                                    on_click=lambda _: self.file_picker.pick_files(allowed_extensions=["conf"]))
            ]),
            flet.VerticalDivider(width=9, thickness=3),
            self.info_column
        ], vertical_alignment=flet.CrossAxisAlignment.START)

    def on_tunnel_click(self, event: flet.ControlEvent):
        tunnel = event.control.data

        self.info_column.controls = [
            flet.Text(value="Interface:",
                      weight=flet.FontWeight.BOLD,
                      size=40),
            flet.Row([
                flet.Text(value="PrivateKey:"),
                flet.Text(value=tunnel.interface.private_key),
            ]),
            flet.Row([
                flet.Text(value="Address:"),
                flet.Text(value=tunnel.interface.address),
            ]),
            flet.Row([
                flet.Text(value="DNS:"),
                flet.Text(value=tunnel.interface.dns),
            ]),
            flet.Row([
                flet.Text(value="MTU:"),
                flet.Text(value=tunnel.interface.mtu),
            ]),

            flet.Text(value="Peer",
                      weight=flet.FontWeight.BOLD,
                      size=40),
            flet.Row([
                flet.Text(value="PublicKey:"),
                flet.Text(value=tunnel.peer.public_key),
            ]),
            flet.Row([
                flet.Text(value="Endpoint:"),
                flet.Text(value=tunnel.peer.endpoint),
            ]),
            flet.Row([
                flet.Text(value="AllowedIPs:"),
                flet.Text(value=tunnel.peer.allowed_ips),
            ]),
            flet.Row([
                flet.Text(value="DisallowedIPs:"),
                flet.Text(value=tunnel.peer.disallowed_ips),
            ]),
            flet.Row([
                flet.Text(value="AllowedApps:"),
                flet.Text(value=tunnel.peer.allowed_apps),
            ]),

            flet.ElevatedButton(text="Edit tunnel", on_click=self.on_tunnel_edit, data=tunnel)
        ]

        self.info_column.update()

    def on_tunnel_add(self, event: flet.FilePickerResultEvent):
        pass

    def on_tunnel_edit(self, event: flet.ControlEvent):
        pass
