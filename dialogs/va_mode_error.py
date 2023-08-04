import flet

import resources


class VAModeErrorDialog(flet.AlertDialog):
    def __init__(self):
        super(VAModeErrorDialog, self).__init__()
        self.title = flet.Text(value=resources.VA_MODE_ERROR_TITLE)
        self.actions = [
            flet.TextButton(resources.CLOSE, on_click=self.close_dlg),
        ]
        self.content = flet.Text(resources.VA_MODE_ERROR_CONTENT)

    def close_dlg(self, event: flet.ControlEvent):
        self.open = False
        self.page.update()
