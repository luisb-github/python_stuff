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

        self.shortcuts_list = ft.ListView(spacing=14, auto_scroll=True)
        self.load_shortcuts_to_list()

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


class Shortcut(ft.UserControl):

    actions_menu_active = False

    def __init__(self, id, title, path):
        super().__init__()
        self.id = id
        self.title = title
        self.path = path

    def build(self):
        self.info_display = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
            controls=[
                ft.Text(self.id, style=ft.TextThemeStyle.LABEL_LARGE,
                        color="White",),
                ft.Text(self.title, style=ft.TextThemeStyle.TITLE_MEDIUM,
                        color="White", expand=True),
            ]
        )

        self.action_list = ft.ResponsiveRow(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN, expand=True)

        self.load_actions_to_list()

        self.actions = ft.Container(
            visible=self.actions_menu_active,
            border_radius=24,
            padding=16,
            bgcolor=ft.colors.BLACK12,
            content=self.action_list
        )

        return ft.Card(
            expand=True,
            content=ft.Container(
                padding=ft.padding.symmetric(vertical=20, horizontal=20),
                border_radius=12,
                on_click=self.actions_menu_toggle,
                content=ft.Column(
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=22,
                    controls=[
                        self.info_display,
                        self.actions
                    ]
                )
            )
        )

    def actions_menu_toggle(self, e):
        self.actions.visible = not self.actions_menu_active
        self.actions_menu_active = not self.actions_menu_active
        self.update()

    def edit(self, e):
        pass

    def delete(self, e):
        pass

    def read_stored_action(self):
        actions = [
            {"action": "open", "hotkey": "o"},
            {"action": "change to", "hotkey": "c"},
            {"action": "move to", "hotkey": "m"},
            {"action": "edit", "hotkey": "e", "type": "edition"},
            {"action": "delete", "hotkey": "d", "type": "edition"},
        ]

        return actions

    def load_actions_to_list(self):
        actions = self.read_stored_action()

        for action in actions:
            action_title = f'{action["action"]} ({action["hotkey"]})'.capitalize(
            )

            if action.get('type'):
                action_button = ft.OutlinedButton(action_title, col={"xs": 6, "sm": 6, "md": 2}, on_click=lambda e: print(
                    "action clicked!"),)
            else:
                action_button = ft.FilledTonalButton(action_title, col={"xs": 12, "sm": 6, "md": 2}, on_click=lambda e: print(
                    "action clicked!"),)

            self.action_list.controls.append(action_button)


def main(page: ft.Page):

    # window settings
    window_position_x = 2100
    window_position_y = 700
    window_width = 360
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
