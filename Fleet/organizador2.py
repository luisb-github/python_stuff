import flet as ft


class ShortcutsView(ft.UserControl):
    def build(self):
        self.banner = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.IconButton(icon=ft.icons.ADD, icon_color="white",
                              icon_size=22, tooltip="Add shortcut",),
                ft.IconButton(icon=ft.icons.SETTINGS, icon_color="white",
                              icon_size=22, tooltip="Settings",)
            ]
        )

        self.shortcuts_list = ft.Column(expand=True, spacing=14)
        self.shortcuts_list.controls.append(ft.Text("self.title", expand=True))
        # self.load_shortcuts_to_list()

        return ft.Column(
            controls=[
                self.banner,
                self.shortcuts_list,
            ]
        )

    def read_stored_shortcuts(self):
        stored_shortcuts = [
            {"title": "Documents", "path": "Documents"},
            {"title": "Vamos Ver", "path": "C:\\Users\\luisb\\Music\\vamosver"},
        ]

        return stored_shortcuts

    def load_shortcuts_to_list(self):
        # grab list of shortcuts
        stored_shortcuts = self.read_stored_shortcuts()

        # append shortcuts to list
        for index, content in enumerate(stored_shortcuts, 1):
            shortcut = Shortcut(index, content["title"], content["path"])
            self.shortcuts_list.controls.append(shortcut)
        # add shortcut to array
        self.update


class Shortcut(ft.UserControl):
    def __init__(self, id, title, path):
        super().__init__()
        self.id = id
        self.title = title
        self.path = path

    def build(self):
        return ft.Text(self.title, expand=True)

    def edit(self, e):
        pass

    def delete(self, e):
        pass


def main(page: ft.Page):

    # window settings
    window_position_x = 2100
    window_position_y = 700
    window_width = 350
    window_height = 700

    # page.window_left = window_position_x
    # page.window_top = window_position_y
    page.window_width = window_width
    page.window_height = window_height
    page.padding = 20
    page.window_resizable = False
    page.title = "Organizador"
    page.window_visible = True
    page.window_always_on_top = True

    page.update()

    # create application instance
    shortcut_view = ShortcutsView()

    # add application's root control to the page
    page.add(shortcut_view)


ft.app(target=main)
