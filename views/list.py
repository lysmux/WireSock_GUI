import shutil
from pathlib import Path

import flet

import wiresock_manager
from utils import app_data_dir


class ListView(flet.UserControl):
    def __init__(self):
        super().__init__()
        self.expand = True

        self.info_column = flet.Column()
        self.tunnels_column = flet.Column(scroll=flet.ScrollMode.AUTO, expand=True)
        self.file_picker = flet.FilePicker(on_result=self.on_tunnel_add)

    def build(self):
        self.update_tunnels()

        return flet.Row([
            flet.Column([
                self.tunnels_column,
                self.file_picker,
                flet.ElevatedButton(text="Add tunnel",
                                    style=flet.ButtonStyle(
                                        color=flet.colors.GREEN
                                    ),
                                    on_click=lambda _: self.file_picker.pick_files(allowed_extensions=["conf"]))
            ]),
            flet.VerticalDivider(width=9, thickness=3),
            self.info_column
        ], vertical_alignment=flet.CrossAxisAlignment.START)

    def update_tunnels(self):
        configs_path = app_data_dir("configs")

        self.tunnels_column.controls.clear()
        for tunnel_path in configs_path.glob("*.conf"):
            tunnel = wiresock_manager.load_config(tunnel_path.stem)
            self.tunnels_column.controls.append(
                flet.TextButton(text=tunnel.name, on_click=self.on_tunnel_click, data=tunnel)
            )
        if self.tunnels_column.page:
            self.tunnels_column.update()

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

            flet.ElevatedButton(text="Edit tunnel",
                                style=flet.ButtonStyle(
                                    color=flet.colors.LIGHT_BLUE
                                ),
                                on_click=self.on_tunnel_edit,
                                data=tunnel),
            flet.ElevatedButton(text="Delete tunnel",
                                style=flet.ButtonStyle(
                                    color=flet.colors.RED
                                ),
                                on_click=self.on_tunnel_delete,
                                data=tunnel)
        ]

        self.info_column.update()

    def on_tunnel_add(self, event: flet.FilePickerResultEvent):
        file = event.files[0]
        configs_path = app_data_dir("configs")
        shutil.copy(file.path, configs_path)
        self.update_tunnels()

    def on_tunnel_edit(self, event: flet.ControlEvent):
        tunnel = event.control.data
        self.page.go(f"/edit/{tunnel.name}")

    def on_tunnel_delete(self, event: flet.ControlEvent):
        tunnel = event.control.data
        configs_path = app_data_dir("configs")

        Path(configs_path, f"{tunnel.name}.conf").unlink()
        self.update_tunnels()
        self.info_column.clean()
