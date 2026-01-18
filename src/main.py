import flet as ft
from core.config_manager import ConfigManager
from core.template_manager import TemplateManager

from ui.views.home import HomeView

def main(page: ft.Page):
    config_mgr = ConfigManager()
    template_mgr = TemplateManager()

    page.title = "Post Generator"

    def route_change(route):
        page.views.clear()
        
        if page.route == "/":
            page.views.append(HomeView(page, config_mgr, template_mgr))

        elif page.route == "/templates":
            page.views.append(ft.View(
                route="/templates",
                controls=[
                    ft.Text("Templates View")
                ]
            ))
        
        page.update()

    page.on_route_change = route_change
    route_change("/")


if __name__ == "__main__":
    ft.app(target=main)
