from pathlib import Path
from shutil import copy

import flet

import config_manager
import resources
from dialogs.tunnel_active import TunnelActiveDialog
from misc import change_tunnel_state
from wiresock_manager.wiresock_manager import WSManager


class ListView(flet.UserControl):
    def __init__(self):
        super().__init__()
        self.expand = True

        self.tunnels_column = flet.Ref[flet.Column]()
        self.info_column = flet.Ref[flet.Column]()
        self.file_picker = flet.FilePicker(on_result=self.add_tunnel)

    def build(self):
        return flet.Row([
            flet.Column([
                self.file_picker,
                flet.Column(ref=self.tunnels_column, scroll=flet.ScrollMode.AUTO, expand=True),
                flet.ElevatedButton(text=resources.ADD_TUNNEL,
                                    style=flet.ButtonStyle(
                                        color=flet.colors.GREEN
                                    ),
                                    on_click=lambda _: self.file_picker.pick_files(allowed_extensions=["conf"]))
            ]),
            flet.VerticalDivider(width=9, thickness=3),
            flet.Column(ref=self.info_column, scroll=flet.ScrollMode.AUTO, expand=True)
        ], vertical_alignment=flet.CrossAxisAlignment.START)

    def did_mount(self):
        self.update_tunnels()

    def update_tunnels(self):
        configs_dir = config_manager.get_configs_dir()

        self.tunnels_column.current.controls.clear()
        for tunnel_path in configs_dir.glob("*.conf"):
            tunnel = config_manager.load_config(tunnel_path.stem)
            self.tunnels_column.current.controls.append(
                flet.TextButton(text=tunnel.name, on_click=self.select_tunnel, data=tunnel)
            )
        if self.tunnels_column.current.page:
            self.tunnels_column.current.update()

    def select_tunnel(self, event: flet.ControlEvent):
        event.control.focus()
        tunnel = event.control.data

        connect_btn = flet.ElevatedButton(text=resources.CONNECT,
                                          style=flet.ButtonStyle(
                                              color=flet.colors.GREEN
                                          ),
                                          on_click=self.activate_tunnel, data=tunnel)
        if tunnel != WSManager().current_tunnel and WSManager().current_tunnel is not None:
            connect_btn.disabled = True
        if tunnel == WSManager().current_tunnel:
            connect_btn.text = resources.DISCONNECT
            connect_btn.style.color = flet.colors.RED

        self.info_column.current.controls = [
            connect_btn,
            flet.Text(value=resources.INTERFACE, weight=flet.FontWeight.BOLD, size=40),
            flet.Row([
                flet.Text(value=resources.PRIVATE_KEY),
                flet.Text(value=tunnel.interface.private_key),
            ], wrap=True),
            flet.Row([
                flet.Text(value=resources.ADDRESS),
                flet.Text(value=tunnel.interface.address),
            ], wrap=True),
            flet.Row([
                flet.Text(value=resources.DNS),
                flet.Text(value=tunnel.interface.dns),
            ], wrap=True),
            flet.Row([
                flet.Text(value=resources.MTU),
                flet.Text(value=tunnel.interface.mtu),
            ], wrap=True),

            flet.Text(value=resources.PEER, weight=flet.FontWeight.BOLD, size=40),
            flet.Row([
                flet.Text(value=resources.PUBLIC_KEY),
                flet.Text(value=tunnel.peer.public_key),
            ], wrap=True),
            flet.Row([
                flet.Text(value=resources.PRESHARED_KEY),
                flet.Text(value=tunnel.peer.pre_shared_key),
            ], wrap=True),
            flet.Row([
                flet.Text(value=resources.ENDPOINT),
                flet.Text(value=tunnel.peer.endpoint),
            ], wrap=True),
            flet.Row([
                flet.Text(value=resources.ALLOWED_IPS),
                flet.Text(value=tunnel.peer.allowed_ips),
            ], wrap=True),
            flet.Row([
                flet.Text(value=resources.DISALLOWED_IPS),
                flet.Text(value=tunnel.peer.disallowed_ips),
            ], wrap=True),
            flet.Row([
                flet.Text(value=resources.ALLOWED_APPS),
                flet.Text(value=tunnel.peer.allowed_apps),
            ], wrap=True),
            flet.Row([
                flet.Text(value=resources.DISALLOWED_APPS),
                flet.Text(value=tunnel.peer.disallowed_apps),
            ], wrap=True),
            flet.Row([
                flet.Text(value=resources.PERSISTENCE_KEEPALIVE),
                flet.Text(value=tunnel.peer.persistent_keepalive),
            ], wrap=True),

            flet.ElevatedButton(text=resources.EDIT_TUNNEL,
                                style=flet.ButtonStyle(
                                    color=flet.colors.LIGHT_BLUE
                                ),
                                on_click=self.edit_tunnel, data=tunnel),
            flet.ElevatedButton(text=resources.DELETE_TUNNEL,
                                style=flet.ButtonStyle(
                                    color=flet.colors.RED
                                ),
                                on_click=self.delete_tunnel, data=tunnel)
        ]

        self.info_column.current.update()

    def add_tunnel(self, event: flet.FilePickerResultEvent):
        if not event.files:
            return

        file = event.files[0]
        configs_dir = config_manager.get_configs_dir()
        copy(file.path, configs_dir)
        self.update_tunnels()

    def edit_tunnel(self, event: flet.ControlEvent):
        tunnel = event.control.data
        if WSManager().current_tunnel == tunnel:
            dlg = TunnelActiveDialog()
            dlg.open = True
            self.page.dialog = dlg
            self.page.update()
        else:
            self.page.go(f"/edit/{tunnel.name}")

    def delete_tunnel(self, event: flet.ControlEvent):
        tunnel = event.control.data
        configs_dir = config_manager.get_configs_dir()

        Path(configs_dir, f"{tunnel.name}.conf").unlink()
        self.update_tunnels()
        self.info_column.current.clean()

    def activate_tunnel(self, event: flet.ControlEvent):
        tunnel = event.control.data

        if WSManager().current_tunnel == tunnel:
            change_tunnel_state(page=self.page, tunnel=tunnel, connect=False)
            event.control.text = resources.CONNECT
            event.control.style.color = flet.colors.GREEN
        elif change_tunnel_state(page=self.page, tunnel=tunnel, connect=True):
            event.control.text = resources.DISCONNECT
            event.control.style.color = flet.colors.RED
            self.page.client_storage.set("last_tunnel", tunnel.name)
        event.control.update()
