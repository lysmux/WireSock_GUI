import shutil
from pathlib import Path

import flet

import config_manager


class ListView(flet.UserControl):
    def __init__(self):
        super().__init__()
        self.expand = True

        self.info_column = flet.Column(scroll=flet.ScrollMode.AUTO, expand=True)
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
        configs_dir = config_manager.get_configs_dir()

        self.tunnels_column.controls.clear()
        for tunnel_path in configs_dir.glob("*.conf"):
            tunnel = config_manager.load_config(tunnel_path.stem)
            self.tunnels_column.controls.append(
                flet.TextButton(text=tunnel.name, on_click=self.on_tunnel_click, data=tunnel)
            )
        if self.tunnels_column.page:
            self.tunnels_column.update()

    def on_tunnel_click(self, event: flet.ControlEvent):
        event.control.focus()
        tunnel = event.control.data

        self.info_column.controls = [
            flet.ElevatedButton(text="Activate",
                                style=flet.ButtonStyle(
                                    color=flet.colors.GREEN
                                ),
                                on_click=self.on_tunnel_state,
                                data=tunnel),
            flet.Text(value="Interface:",
                      weight=flet.FontWeight.BOLD,
                      size=40),
            flet.Row([
                flet.Text(value="Private key:"),
                flet.Text(value=tunnel.interface.private_key),
            ], wrap=True),
            flet.Row([
                flet.Text(value="Address:"),
                flet.Text(value=tunnel.interface.address),
            ], wrap=True),
            flet.Row([
                flet.Text(value="DNS:"),
                flet.Text(value=tunnel.interface.dns),
            ], wrap=True),
            flet.Row([
                flet.Text(value="MTU:"),
                flet.Text(value=tunnel.interface.mtu),
            ], wrap=True),

            flet.Text(value="Peer",
                      weight=flet.FontWeight.BOLD,
                      size=40),
            flet.Row([
                flet.Text(value="Public key:"),
                flet.Text(value=tunnel.peer.public_key),
            ], wrap=True),
            flet.Row([
                flet.Text(value="Preshared key:"),
                flet.Text(value=tunnel.peer.pre_shared_key),
            ], wrap=True),
            flet.Row([
                flet.Text(value="Endpoint:"),
                flet.Text(value=tunnel.peer.endpoint),
            ], wrap=True),
            flet.Row([
                flet.Text(value="Allowed IPs:"),
                flet.Text(value=tunnel.peer.allowed_ips),
            ], wrap=True),
            flet.Row([
                flet.Text(value="Disallowed IPs:"),
                flet.Text(value=tunnel.peer.disallowed_ips),
            ], wrap=True),
            flet.Row([
                flet.Text(value="Allowed apps:"),
                flet.Text(value=tunnel.peer.allowed_apps),
            ], wrap=True),
            flet.Row([
                flet.Text(value="Disallowed apps:"),
                flet.Text(value=tunnel.peer.disallowed_apps),
            ], wrap=True),
            flet.Row([
                flet.Text(value="Persistence keepalive:"),
                flet.Text(value=tunnel.peer.persistent_keepalive),
            ], wrap=True),

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
        if not event.files:
            return

        file = event.files[0]
        configs_dir = config_manager.get_configs_dir()
        shutil.copy(file.path, configs_dir)
        self.update_tunnels()

    def on_tunnel_edit(self, event: flet.ControlEvent):
        tunnel = event.control.data
        self.page.go(f"/edit/{tunnel.name}")

    def on_tunnel_delete(self, event: flet.ControlEvent):
        tunnel = event.control.data
        configs_dir = config_manager.get_configs_dir()

        Path(configs_dir, f"{tunnel.name}.conf").unlink()
        self.update_tunnels()
        self.info_column.clean()

    def on_tunnel_state(self, event: flet.ControlEvent):
        pass
