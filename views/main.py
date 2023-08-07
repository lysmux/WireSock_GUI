import flet

import resources
from views.list import ListView
from views.logger import LoggerView
from views.settings import SettingsView
from views.statistics import StatisticsView


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
                text=resources.TAB_STATISTICS,
                icon=flet.icons.SHOW_CHART,
                content=flet.Container(StatisticsView(), padding=flet.padding.all(10))
            ),
            flet.Tab(
                text=resources.TAB_LOG,
                icon=flet.icons.NOTES,
                content=flet.Container(LoggerView(), padding=flet.padding.all(10))
            ),
            flet.Tab(
                text=resources.TAB_SETTINGS,
                icon=flet.icons.SETTINGS,
                content=flet.Container(SettingsView(), padding=flet.padding.all(10))
            ),
        ]
        self.expand = True
