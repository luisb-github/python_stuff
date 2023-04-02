import flet as ft

class shortcuts_view(ft.UserControl):
    def build(self):
        self.banner = ft.TextField()
        self.shortcuts_list = ft.TextField()

        return ft.Column(
            controls=[
                self.banner,
                self.shortcuts_list
            ]
        )


def main(page: ft.Page):
    page.add(ft.Text(value="Hello, world!"))

ft.app(target=main)