import flet

from views.list import ListView
from views.logger import LoggerView


class MainView(flet.Tabs):
    def __init__(self):
        super(MainView, self).__init__()
        self.tabs = [
            flet.Tab(
                text="List tunnels",
                icon=flet.icons.LIST,
                content=flet.Container(ListView(), padding=flet.padding.all(10))
            ),
            flet.Tab(
                text="Logs",
                icon=flet.icons.NOTES,
                content=flet.Container(LoggerView(), padding=flet.padding.all(10))
            ),
        ]
        self.expand = True
