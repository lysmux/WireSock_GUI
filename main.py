import flet
from flet_core import TemplateRoute

from utils import config_manager
import resources
from misc import change_tunnel_state
from views.edit import EditView
from views.main import MainView


def route_change(route: flet.RouteChangeEvent):
    template_route = TemplateRoute(route.route)

    route.page.views.clear()
    route.page.views.append(
        flet.View(
            "/",
            [
                MainView()
            ],
            padding=flet.padding.all(0)
        )
    )
    if template_route.match("/edit/:config_name"):
        route.page.views.append(
            flet.View(
                "/edit",
                [
                    EditView(template_route.config_name)
                ],
                scroll=flet.ScrollMode.AUTO
            )
        )
    route.page.update()


def on_startup(page: flet.Page):
    autoconnect = page.client_storage.get("autoconnect")
    if autoconnect is not False:
        last_tunnel_name = page.client_storage.get("last_tunnel")
        last_tunnel = config_manager.load_config(last_tunnel_name)
        if last_tunnel:
            change_tunnel_state(page=page, tunnel=last_tunnel, connect=True)


def main(page: flet.Page):
    page.title = resources.APP_TITLE

    page.on_route_change = route_change
    page.go(page.route)

    on_startup(page)


flet.app(main)
