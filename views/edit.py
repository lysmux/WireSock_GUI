import flet

from utils import config_manager
import resources
from dialogs.list_edit import ListEditDialog


class EditView(flet.UserControl):
    def __init__(self, config_name: str):
        super().__init__()
        self.tf_private_key = flet.Ref[flet.TextField]()
        self.tf_address = flet.Ref[flet.TextField]()
        self.tf_dns = flet.Ref[flet.TextField]()
        self.tf_mtu = flet.Ref[flet.TextField]()
        self.tf_public_key = flet.Ref[flet.TextField]()
        self.tf_pre_shared_key = flet.Ref[flet.TextField]()
        self.tf_endpoint = flet.Ref[flet.TextField]()
        self.tf_allowed_ips = flet.Ref[flet.TextField]()
        self.tf_disallowed_ips = flet.Ref[flet.TextField]()
        self.tf_allowed_apps = flet.Ref[flet.TextField]()
        self.tf_disallowed_apps = flet.Ref[flet.TextField]()
        self.tf_persist = flet.Ref[flet.TextField]()

        self.btn_save = flet.Ref[flet.ElevatedButton]()

        self.tunnel = config_manager.load_config(config_name)

    def build(self):
        interface_grid = flet.GridView([
            flet.Column([
                flet.Text(value=resources.PRIVATE_KEY),
                flet.TextField(ref=self.tf_private_key, value=self.tunnel.interface.private_key)
            ]),
            flet.Column([
                flet.Text(value=resources.ADDRESS),
                flet.TextField(ref=self.tf_address, value=str(self.tunnel.interface.address),
                               on_focus=self.on_list_field_focus, data=self.tunnel.interface.address)
            ]),
            flet.Column([
                flet.Text(value=resources.DNS),
                flet.TextField(ref=self.tf_dns, value=str(self.tunnel.interface.dns),
                               on_focus=self.on_list_field_focus,
                               data=self.tunnel.interface.dns)
            ]),
            flet.Column([
                flet.Text(value=resources.MTU),
                flet.TextField(ref=self.tf_mtu, value=str(self.tunnel.interface.mtu),
                               hint_text=resources.OPTIONAL)
            ]),
        ], max_extent=350, run_spacing=20, child_aspect_ratio=2.5)

        peer_grid = flet.GridView([
            flet.Column([
                flet.Text(value=resources.PUBLIC_KEY),
                flet.TextField(ref=self.tf_public_key, value=self.tunnel.peer.public_key)
            ]),
            flet.Column([
                flet.Text(value=resources.PRESHARED_KEY),
                flet.TextField(ref=self.tf_pre_shared_key, value=self.tunnel.peer.pre_shared_key,
                               hint_text=resources.OPTIONAL)
            ]),
            flet.Column([
                flet.Text(value=resources.ENDPOINT),
                flet.TextField(ref=self.tf_endpoint, value=self.tunnel.peer.endpoint)
            ]),
            flet.Column([
                flet.Text(value=resources.ALLOWED_IPS),
                flet.TextField(ref=self.tf_allowed_ips, value=str(self.tunnel.peer.allowed_ips),
                               on_focus=self.on_list_field_focus,
                               data=self.tunnel.peer.allowed_ips)
            ]),
            flet.Column([
                flet.Text(value=resources.DISALLOWED_IPS),
                flet.TextField(ref=self.tf_disallowed_ips, value=str(self.tunnel.peer.disallowed_ips),
                               on_focus=self.on_list_field_focus,
                               data=self.tunnel.peer.disallowed_ips)
            ]),
            flet.Column([
                flet.Text(value=resources.ALLOWED_APPS),
                flet.TextField(ref=self.tf_allowed_apps, value=str(self.tunnel.peer.allowed_apps),
                               on_focus=self.on_list_field_focus,
                               data=self.tunnel.peer.allowed_apps)
            ]),
            flet.Column([
                flet.Text(value=resources.DISALLOWED_APPS),
                flet.TextField(ref=self.tf_disallowed_apps, value=str(self.tunnel.peer.disallowed_apps),
                               on_focus=self.on_list_field_focus,
                               data=self.tunnel.peer.disallowed_apps)
            ]),
            flet.Column([
                flet.Text(value=resources.PERSISTENCE_KEEPALIVE),
                flet.TextField(ref=self.tf_persist, value=str(self.tunnel.peer.persistent_keepalive),
                               hint_text=resources.OPTIONAL)
            ]),
        ], max_extent=350, run_spacing=20, child_aspect_ratio=2.5)

        return flet.Column(
            [
                flet.ElevatedButton(text=resources.BACK, icon=flet.icons.KEYBOARD_ARROW_LEFT,
                                    style=flet.ButtonStyle(
                                        color=flet.colors.LIGHT_BLUE
                                    ),
                                    on_click=lambda _: self.page.go("/")),

                flet.Text(value=f"{resources.TUNNEL}: {self.tunnel.name}", weight=flet.FontWeight.BOLD, size=40),

                flet.Text(value=resources.INTERFACE, weight=flet.FontWeight.BOLD, size=40),
                interface_grid,

                flet.Divider(height=9, thickness=3),

                flet.Text(value=resources.PEER, weight=flet.FontWeight.BOLD, size=40),
                peer_grid,

                flet.ElevatedButton(ref=self.btn_save, text=resources.SAVE,
                                    style=flet.ButtonStyle(
                                        color=flet.colors.GREEN
                                    ),
                                    on_click=self.save)
            ],
        )

    def on_list_field_focus(self, event: flet.ControlEvent):
        self.btn_save.current.focus()  # unfocus text field
        dlg = ListEditDialog(event.control)
        dlg.open = True
        self.page.dialog = dlg
        self.page.update()

    def save(self, event: flet.ControlEvent):
        has_error = False

        for field in [
            self.tf_private_key.current,
            self.tf_public_key.current,
            self.tf_endpoint.current,
            self.tf_address.current
        ]:
            if not field.value:
                has_error = True
                field.error_text = resources.NOT_EMPTY
                field.update()

        for field in [
            self.tf_mtu.current,
            self.tf_persist.current
        ]:
            if field.value and not field.value.isdigit():
                has_error = True
                field.error_text = resources.ONLY_POSITIVE_INTEGER
                field.update()

        if not has_error:
            self.tunnel.interface.private_key = self.tf_private_key.current.value
            self.tunnel.interface.address = self.tf_address.current.data
            self.tunnel.interface.dns = self.tf_dns.current.data
            self.tunnel.interface.mtu = int(self.tf_mtu.current.value)

            self.tunnel.peer.public_key = self.tf_public_key.current.value
            self.tunnel.peer.pre_shared_key = self.tf_pre_shared_key.current.value
            self.tunnel.peer.endpoint = self.tf_endpoint.current.value
            self.tunnel.peer.allowed_ips = self.tf_allowed_ips.current.data
            self.tunnel.peer.disallowed_ips = self.tf_disallowed_ips.current.data
            self.tunnel.peer.allowed_apps = self.tf_allowed_apps.current.data
            self.tunnel.peer.disallowed_apps = self.tf_disallowed_apps.current.data
            self.tunnel.peer.persistent_keepalive = int(self.tf_persist.current.value)

            config_manager.save_config(self.tunnel)

            self.page.go("/")
