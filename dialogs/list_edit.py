import flet

import resources


class ListEditDialog(flet.AlertDialog):
    def __init__(self, list_field: flet.TextField):
        super(ListEditDialog, self).__init__()
        self.title = flet.Text(resources.EDIT)
        self.actions = [
            flet.ElevatedButton(text=resources.UPDATE, on_click=self.close_dlg)
        ]
        self.content = flet.Column([
            flet.ElevatedButton(text=resources.ADD, on_click=self.add_field)
        ])
        for field in list_field.data:
            self.content.controls.insert(0, flet.TextField(value=field, on_blur=self.on_field_blur))

        self.list_field = list_field

    def add_field(self, event: flet.ControlEvent):
        new_field = flet.TextField(on_blur=self.on_field_blur)
        self.content.controls.insert(-1, new_field)
        self.content.update()
        new_field.focus()

    def on_field_blur(self, event: flet.ControlEvent):
        if not event.control.value.strip():
            self.content.controls.remove(event.control)
            self.content.update()

    def close_dlg(self, event: flet.ControlEvent):
        self.open = False
        self.page.update()

        data = []
        for control in self.content.controls:
            if isinstance(control, flet.TextField):
                data.append(control.value)
        self.list_field.data = data
        self.list_field.value = str(data)
        self.list_field.update()
