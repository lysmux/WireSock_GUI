import flet

from views.tunnels import TunnelsView


def main(page: flet.Page):
    page.title = "WireSock"

    tunnels_view = TunnelsView()
    page.add(tunnels_view)


flet.app(main)
