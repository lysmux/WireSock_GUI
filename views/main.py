import flet

import resources
from views.list import ListView
from views.logger import LoggerView


class MainView(flet.Tabs):
    def __init__(self):
        super(MainView, self).__init__()
        self.tabs = [
            flet.Tab(
                text=resources.TAB_TUNNELS,
                icon=flet.icons.LIST,
                content=flet.Container(ListView(), padding=flet.padding.all(10))
            ),
            flet.Tab(
                text=resources.TAB_LOG,
                icon=flet.icons.NOTES,
                content=flet.Container(LoggerView(), padding=flet.padding.all(10))
            ),
        ]
        self.expand = True
