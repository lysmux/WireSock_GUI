import flet

import config_manager
import resources
from dialogs.list_edit import ListEditDialog


class EditView(flet.UserControl):
    def __init__(self, config_name: str):
        super().__init__()

        self.tunnel = config_manager.load_config(config_name)

        self.tf_private_key = flet.TextField(value=self.tunnel.interface.private_key)
        self.tf_address = flet.TextField(value=str(self.tunnel.interface.address),
                                         on_focus=self.on_list_field_focus,
                                         data=self.tunnel.interface.address)
        self.tf_dns = flet.TextField(value=str(self.tunnel.interface.dns),
                                     on_focus=self.on_list_field_focus,
                                     data=self.tunnel.interface.dns)
        self.tf_mtu = flet.TextField(value=str(self.tunnel.interface.mtu), hint_text=resources.OPTIONAL)

        self.tf_public_key = flet.TextField(value=self.tunnel.peer.public_key)
        self.tf_pre_shared_key = flet.TextField(value=self.tunnel.peer.pre_shared_key, hint_text=resources.OPTIONAL)
        self.tf_endpoint = flet.TextField(value=self.tunnel.peer.endpoint)
        self.tf_allowed_ips = flet.TextField(value=str(self.tunnel.peer.allowed_ips),
                                             on_focus=self.on_list_field_focus,
                                             data=self.tunnel.peer.allowed_ips)
        self.tf_disallowed_ips = flet.TextField(value=str(self.tunnel.peer.disallowed_ips),
                                                on_focus=self.on_list_field_focus,
                                                data=self.tunnel.peer.disallowed_ips)
        self.tf_allowed_apps = flet.TextField(value=str(self.tunnel.peer.allowed_apps),
                                              on_focus=self.on_list_field_focus,
                                              data=self.tunnel.peer.allowed_apps)
        self.tf_disallowed_apps = flet.TextField(value=str(self.tunnel.peer.disallowed_apps),
                                                 on_focus=self.on_list_field_focus,
                                                 data=self.tunnel.peer.disallowed_apps)
        self.tf_persist = flet.TextField(value=str(self.tunnel.peer.persistent_keepalive), hint_text=resources.OPTIONAL)

        self.save_btn = flet.ElevatedButton(text=resources.SAVE,
                                            style=flet.ButtonStyle(
                                                color=flet.colors.GREEN
                                            ),
                                            on_click=self.on_save)

    def build(self):
        return flet.Column(
            [
                flet.ElevatedButton(text=resources.BACK,
                                    icon=flet.icons.KEYBOARD_ARROW_LEFT,
                                    style=flet.ButtonStyle(
                                        color=flet.colors.LIGHT_BLUE
                                    ),
                                    on_click=lambda _: self.page.go("/")),

                flet.Text(value=f"{resources.TUNNEL}: {self.tunnel.name}",
                          weight=flet.FontWeight.BOLD,
                          size=40),

                flet.Text(value=resources.INTERFACE,
                          weight=flet.FontWeight.BOLD,
                          size=40),
                flet.GridView([
                    flet.Column([
                        flet.Text(value=resources.PRIVATE_KEY),
                        self.tf_private_key
                    ]),
                    flet.Column([
                        flet.Text(value=resources.ADDRESS),
                        self.tf_address
                    ]),
                    flet.Column([
                        flet.Text(value=resources.DNS),
                        self.tf_dns
                    ]),
                    flet.Column([
                        flet.Text(value=resources.MTU),
                        self.tf_mtu
                    ]),
                ],
                    max_extent=350,
                    run_spacing=20,
                    child_aspect_ratio=2.5),

                flet.Divider(height=9, thickness=3),

                flet.Text(value=resources.PEER,
                          weight=flet.FontWeight.BOLD,
                          size=40),
                flet.GridView([
                    flet.Column([
                        flet.Text(value=resources.PUBLIC_KEY),
                        self.tf_public_key
                    ]),
                    flet.Column([
                        flet.Text(value=resources.PRESHARED_KEY),
                        self.tf_pre_shared_key
                    ]),
                    flet.Column([
                        flet.Text(value=resources.ENDPOINT),
                        self.tf_endpoint
                    ]),
                    flet.Column([
                        flet.Text(value=resources.ALLOWED_IPS),
                        self.tf_allowed_ips
                    ]),
                    flet.Column([
                        flet.Text(value=resources.DISALLOWED_IPS),
                        self.tf_disallowed_ips
                    ]),
                    flet.Column([
                        flet.Text(value=resources.ALLOWED_APPS),
                        self.tf_allowed_apps
                    ]),
                    flet.Column([
                        flet.Text(value=resources.DISALLOWED_APPS),
                        self.tf_disallowed_apps
                    ]),
                    flet.Column([
                        flet.Text(value=resources.PERSISTENCE_KEEPALIVE),
                        self.tf_persist
                    ]),
                ],
                    max_extent=350,
                    run_spacing=20,
                    child_aspect_ratio=2.5),
                self.save_btn
            ],
        )

    def on_list_field_focus(self, event: flet.ControlEvent):
        self.save_btn.focus()  # unfocus text field
        dlg = ListEditDialog(event.control)
        dlg.open = True
        self.page.dialog = dlg
        self.page.update()

    def on_save(self, event: flet.ControlEvent):
        has_error = False

        for field in [
            self.tf_private_key,
            self.tf_public_key,
            self.tf_endpoint,
            self.tf_address
        ]:
            if not field.value:
                has_error = True
                field.error_text = resources.NOT_EMPTY
                field.update()

        for field in [
            self.tf_mtu,
            self.tf_persist
        ]:
            if field.value and not field.value.isdigit():
                has_error = True
                field.error_text = resources.ONLY_POSITIVE_INTEGER
                field.update()

        if not has_error:
            self.tunnel.interface.private_key = self.tf_private_key.value
            self.tunnel.interface.address = self.tf_address.data
            self.tunnel.interface.dns = self.tf_dns.data
            self.tunnel.interface.mtu = int(self.tf_mtu.value)

            self.tunnel.peer.public_key = self.tf_public_key.value
            self.tunnel.peer.pre_shared_key = self.tf_pre_shared_key.value
            self.tunnel.peer.endpoint = self.tf_endpoint.value
            self.tunnel.peer.allowed_ips = self.tf_allowed_ips.data
            self.tunnel.peer.disallowed_ips = self.tf_disallowed_ips.data
            self.tunnel.peer.allowed_apps = self.tf_allowed_apps.data
            self.tunnel.peer.disallowed_apps = self.tf_disallowed_apps.data
            self.tunnel.peer.persistent_keepalive = int(self.tf_persist.value)

            config_manager.save_config(self.tunnel)

            self.page.go("/")
