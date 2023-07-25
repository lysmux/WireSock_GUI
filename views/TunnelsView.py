import flet

from models import Tunnel


class TunnelsView(flet.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        return flet.Row([
            flet.Column([
                flet.ElevatedButton(text="Add tunnel")
            ]),
            flet.Column([

            ])
        ])
