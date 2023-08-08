import flet
from flet_core import TemplateRoute

import resources
from views.edit import EditView
from views.main import MainView


def on_startup(page: flet.Page):
    pass


def route_change(route: flet.RouteChangeEvent):
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

    page.on_route_change = route_change
    page.go(page.route)

    on_startup(page)


flet.app(main)
