import flet

import resources


class AlreadyRunningDialog(flet.AlertDialog):
    def __init__(self):
        super().__init__(open=True)
        self.title = flet.Text(resources.ALREADY_RUNNING_TITLE)
        self.actions = [
            flet.TextButton(resources.EXIT, on_click=self.exit),
        ]
        self.content = flet.Text(resources.ALREADY_RUNNING_CONTENT)
        self.modal = True

    def exit(self, event: flet.ControlEvent):
        self.page.window_destroy()
