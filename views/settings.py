import sys
from pathlib import Path

import flet
import winshell

import resources
from dialogs.va_mode_error import VAModeErrorDialog
from wiresock_manager.wiresock_manager import WSManager


class SettingsView(flet.UserControl):
    def __init__(self):
        super(SettingsView, self).__init__()

        self.autostart = flet.Ref[flet.Switch]()
        self.autoconnect = flet.Ref[flet.Switch]()
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
                flet.Text(resources.AUTOCONNECT),
                flet.Switch(ref=self.autoconnect, on_change=self.on_autoconnect_change)
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
                        flet.dropdown.Option(text=resources.LEVEL_ERROR, key="error"),
                        flet.dropdown.Option(text=resources.LEVEL_INFO, key="info"),
                        flet.dropdown.Option(text=resources.LEVEL_ALL, key="all"),
                    ],
                    value="All",
                    on_change=self.on_log_level_change
                )
            ])
        ])

    def did_mount(self):
        self.load_settings()

    def load_settings(self):
        autostart = self.page.client_storage.get("autostart") or False
        autoconnect = self.page.client_storage.get("autoconnect") or False
        check_updates = self.page.client_storage.get("check_updates") or False
        va_mode = self.page.client_storage.get("va_mode") or False
        log_level = self.page.client_storage.get("log_level") or resources.LEVEL_ERROR

        self.autostart.current.value = autostart
        self.autostart.current.update()

        self.autoconnect.current.value = autoconnect
        self.autoconnect.current.update()

        self.check_updates.current.value = check_updates
        self.check_updates.current.update()

        self.va_mode.current.value = va_mode
        self.va_mode.current.update()

        self.log_level.current.value = log_level
        self.log_level.current.update()

        WSManager().set_va_mode(va_mode)
        WSManager().set_log_level(log_level)

    def on_autostart_change(self, event: flet.ControlEvent):
        if getattr(sys, "frozen", False):
            file_name = Path(sys.executable).with_suffix(".lnk").name
            startup_path = Path(winshell.startup(), file_name)
            if not event.control.value:
                startup_path.unlink(missing_ok=True)
            else:
                with winshell.shortcut(startup_path) as link:
                    link.path = sys.executable

        self.page.client_storage.set("autostart", event.control.value)

    def on_autoconnect_change(self, event: flet.ControlEvent):
        self.page.client_storage.set("autoconnect", event.control.value)

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
        self.page.client_storage.set("log_level", event.control.data)
        WSManager().set_log_level(event.control.data)
