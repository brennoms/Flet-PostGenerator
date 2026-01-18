import flet as ft


class HomeView(ft.View):
    def controls(self, page, config_mgr, template_mgr):
        return [
            ft.Text("Welcome to the Home View"),
            ft.Text(str(config_mgr.configs)),
            ft.Text(str(template_mgr.templates)),
            ft.ElevatedButton(
                "Go to Templates",
                on_click=lambda e: page.go("/templates")
            )
        ]

    def __init__(self, page, config_mgr, template_mgr):
        super().__init__(
            route="/",
            controls= self.controls(page, config_mgr, template_mgr)
        )
