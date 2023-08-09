import flet
from flet_core import TemplateRoute

import resources
from dialogs.not_installed import NotInstalledDialog
from utils.misc import get_wiresock_bin
from views.edit import EditView
from views.main import MainView


def check_startup(page: flet.Page) -> bool:
    if not get_wiresock_bin():
        dlg = NotInstalledDialog()
        dlg.open = True
        page.dialog = dlg
        page.update()
        return False
    return True


def on_route_change(route: flet.RouteChangeEvent):
    template_route = TemplateRoute(route.route)

    route.page.views.clear()
    route.page.views.append(
        flet.View(
            "/",
            [MainView()],
            padding=flet.padding.all(0)
        )
    )
    if template_route.match("/edit/:config_name"):
        route.page.views.append(
            flet.View(
                "/edit",
                [EditView(getattr(template_route, "config_name"))],
                scroll=flet.ScrollMode.AUTO
            )
        )
    route.page.update()


def main(page: flet.Page):
    page.title = resources.APP_TITLE
    page.on_route_change = on_route_change

    if check_startup(page):
        page.go(page.route)


flet.app(main)
