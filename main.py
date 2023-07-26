import flet
from flet_core import TemplateRoute

from views.edit import EditView
from views.list import ListView


def main(page: flet.Page):
    page.title = "WireSock"

    def route_change(route):
        template_route = TemplateRoute(route.route)

        page.views.clear()
        page.views.append(
            flet.View(
                "/",
                [
                    ListView()
                ],
            )
        )
        if template_route.match("/edit/:tunnel_name"):
            page.views.append(
                flet.View(
                    "/edit",
                    [
                        EditView(template_route.tunnel_name)
                    ],
                )
            )
        page.update()

    page.on_route_change = route_change
    page.go(page.route)


flet.app(main)
