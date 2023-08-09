from pathlib import Path
from shutil import copy

import flet

import resources
from dialogs.tunnel_active import TunnelActiveDialog
from dialogs.tunnel_create import TunnelCreateDialog
from dialogs.tunnel_error import TunnelErrorDialog
from models import Tunnel
from utils import config_manager
from utils.notify import notify
from wiresock_manager.wiresock_manager import WSManager


class ListView(flet.UserControl):
    _first_start = True

    def __init__(self):
        super().__init__()
        self.tunnels_column = flet.Ref[flet.Column]()
        self.info_column = flet.Ref[flet.Column]()
        self.connect_btn = flet.Ref[flet.ElevatedButton]()
        self.file_picker = flet.FilePicker(on_result=self.add_tunnel)

    def build(self):
        return flet.Row([
            flet.Column([
                self.file_picker,
                flet.Column(ref=self.tunnels_column, scroll=flet.ScrollMode.AUTO, expand=True),
                flet.ElevatedButton(text=resources.ADD_TUNNEL,
                                    style=flet.ButtonStyle(color=flet.colors.GREEN),
                                    on_click=lambda _: self.file_picker.pick_files(allowed_extensions=["conf"])),
                flet.ElevatedButton(text=resources.CREATE_TUNNEL,
                                    style=flet.ButtonStyle(color=flet.colors.GREEN),
                                    on_click=self.create_tunnel
                                    )
            ]),
            flet.VerticalDivider(width=9, thickness=3),
            flet.Column(ref=self.info_column, scroll=flet.ScrollMode.AUTO, expand=True)
        ], vertical_alignment=flet.CrossAxisAlignment.START)

    def did_mount(self):
        if self._first_start:
            self.__class__._first_start = False
            autoconnect = self.page.client_storage.get("autoconnect")
            if autoconnect is not False:
                last_tunnel_name = self.page.client_storage.get("last_tunnel")
                last_tunnel = config_manager.load_config(last_tunnel_name)
                if last_tunnel:
                    self.activate_tunnel(last_tunnel)

        self.update_tunnels()

    def update_tunnels(self):
        configs_dir = config_manager.get_configs_dir()
        current_tunnel_btn = None

        self.tunnels_column.current.controls.clear()
        for tunnel_path in configs_dir.glob("*.conf"):
            tunnel = config_manager.load_config(tunnel_path.stem)

            tunnel_btn = flet.TextButton(text=tunnel.name, on_click=self.select_tunnel, data=tunnel)
            self.tunnels_column.current.controls.append(tunnel_btn)
            if WSManager().current_tunnel == tunnel:
                current_tunnel_btn = tunnel_btn
        self.tunnels_column.current.update()

        if current_tunnel_btn:
            current_tunnel_btn.focus()
            current_tunnel_btn.update()

    def select_tunnel(self, event: flet.ControlEvent):
        event.control.focus()
        tunnel = event.control.data

        self.info_column.current.controls = [
            flet.ElevatedButton(ref=self.connect_btn, text=resources.CONNECT,
                                style=flet.ButtonStyle(color=flet.colors.GREEN),
                                on_click=self.change_tunnel_state, data=tunnel),
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
                                style=flet.ButtonStyle(color=flet.colors.LIGHT_BLUE),
                                on_click=self.edit_tunnel, data=tunnel),
            flet.ElevatedButton(text=resources.DELETE_TUNNEL,
                                style=flet.ButtonStyle(color=flet.colors.RED),
                                on_click=self.delete_tunnel, data=tunnel)
        ]
        self.info_column.current.update()

        if tunnel != WSManager().current_tunnel and WSManager().current_tunnel is not None:
            self.connect_btn.current.disabled = True
        if tunnel == WSManager().current_tunnel:
            self.connect_btn.current.text = resources.DISCONNECT
            self.connect_btn.current.style.color = flet.colors.RED
        self.connect_btn.current.update()

    def add_tunnel(self, event: flet.FilePickerResultEvent):
        if not event.files:
            return

        file = event.files[0]
        configs_dir = config_manager.get_configs_dir()
        copy(file.path, configs_dir)
        self.update_tunnels()

    def create_tunnel(self, event: flet.FilePickerResultEvent):
        dlg = TunnelCreateDialog()
        dlg.open = True
        self.page.dialog = dlg
        self.page.update()

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

    def change_tunnel_state(self, event: flet.ControlEvent):
        tunnel = event.control.data

        if WSManager().current_tunnel == tunnel:
            self.deactivate_tunnel(tunnel)
            event.control.text = resources.CONNECT
            event.control.style.color = flet.colors.GREEN
        elif self.activate_tunnel(tunnel):
            event.control.text = resources.DISCONNECT
            event.control.style.color = flet.colors.RED
            self.page.client_storage.set("last_tunnel", tunnel.name)
        event.control.update()

    def activate_tunnel(self, tunnel: Tunnel):
        WSManager().set_va_mode(self.page.client_storage.get("va_mode") or False)
        log_level = self.page.client_storage.get("log_level") or "all"

        if not WSManager().connect_tunnel(tunnel=tunnel, log_level=log_level):
            dlg = TunnelErrorDialog(tunnel)
            dlg.open = True
            self.page.dialog = dlg
            self.page.update()
            return False

        notify(tunnel=tunnel, message=resources.CONNECT_NOTIFY)
        return True

    def deactivate_tunnel(self, tunnel):
        WSManager().disconnect_tunnel()
        notify(tunnel=tunnel, message=resources.DISCONNECT_NOTIFY)
