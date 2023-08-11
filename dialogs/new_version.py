import flet

import resources


class NewVersionDialog(flet.AlertDialog):
    def __init__(self, release_url: str):
        super().__init__(open=True)
        self.title = flet.Text(resources.NOT_INSTALLED_TITLE)
        self.actions = [
            flet.TextButton(resources.DOWNLOAD, url=release_url),
            flet.TextButton(resources.CLOSE, on_click=self.close_dlg),
        ]
        self.content = flet.Text(resources.NOT_INSTALLED_CONTENT)

    def close_dlg(self, event: flet.ControlEvent):
        self.open = False
        self.page.update()
