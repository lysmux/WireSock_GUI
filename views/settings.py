import flet

import resources
from dialogs.va_mode_error import VAModeErrorDialog
from wiresock_manager.wiresock_manager import WSManager


class SettingsView(flet.UserControl):
    def __init__(self):
        super(SettingsView, self).__init__()

        self.autostart = flet.Ref[flet.Switch]()
        self.check_updates = flet.Ref[flet.Switch]()
        self.va_mode = flet.Ref[flet.Switch]()
        self.log_level = flet.Ref[flet.Dropdown]()

    def build(self):
        return flet.Column([
            flet.Row([
                flet.Text(resources.AUTOSTART),
                flet.Switch(ref=self.autostart, on_change=self.on_autostart_change)
            ]),
            flet.Row([
                flet.Text(resources.CHECK_UPDATES),
                flet.Switch(ref=self.check_updates, on_change=self.on_check_updates_change)
            ]),
            flet.Row([
                flet.Text(resources.VA_MODE),
                flet.Switch(ref=self.va_mode, on_change=self.on_va_mode_change)
            ]),
            flet.Row([
                flet.Text(resources.LOG_LEVEL),
                flet.Dropdown(
                    ref=self.log_level,
                    options=[
                        flet.dropdown.Option(resources.LEVEL_ERROR),
                        flet.dropdown.Option(resources.LEVEL_INFO),
                        flet.dropdown.Option(resources.LEVEL_ALL),
                    ],
                    value=resources.LEVEL_ERROR,
                    on_change=self.on_log_level_change
                )
            ])
        ])

    def on_autostart_change(self, event: flet.ControlEvent):
        self.page.client_storage.set("autostart", event.control.value)

    def on_check_updates_change(self, event: flet.ControlEvent):
        self.page.client_storage.set("check_updates", event.control.value)

    def on_va_mode_change(self, event: flet.ControlEvent):
        if WSManager().current_tunnel:
            event.control.value = not event.control.value
            event.control.update()

            dlg = VAModeErrorDialog()
            dlg.open = True
            self.page.dialog = dlg
            self.page.update()
        else:
            WSManager().set_va_mode(event.control.value)
            self.page.client_storage.set("va_mode", event.control.value)

    def on_log_level_change(self, event: flet.ControlEvent):
        self.page.client_storage.set("log_level", event.control.value)
