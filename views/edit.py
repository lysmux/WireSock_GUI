import flet


class EditView(flet.UserControl):
    def __init__(self, tunnel_name: str):
        super().__init__()
        print(tunnel_name)

    def build(self):
        return flet.Text(value="EDIT")
