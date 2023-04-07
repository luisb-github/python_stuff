import flet as ft
import tkinter as tk
from tkinter import filedialog

main_page = ft.page


class ShortcutsView(ft.UserControl):

    stored_shortcuts = []

    def build(self):
        self.banner = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.OutlinedButton("Add (a)", icon=ft.icons.ADD,
                                  on_click=self.add_shortcut),
                ft.IconButton(icon=ft.icons.SETTINGS, icon_color="white",
                              icon_size=22, tooltip="Settings",)
            ]
        )

        self.shortcuts_list = ft.ListView(spacing=14, auto_scroll=True)
        self.load_shortcuts_to_list()

        return ft.Column(
            spacing=34,
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

        # check if there is stored shortcuts
        if not stored_shortcuts:
            no_shortctuts_text = ft.Text("No shortcuts created", expand=True,
                                         text_align=ft.TextAlign.CENTER, style=ft.TextThemeStyle.LABEL_LARGE, )
            self.shortcuts_list.controls.append(no_shortctuts_text)
            return

        # append shortcuts to list
        for index, content in enumerate(stored_shortcuts, 1):
            title = content.get("title", "no title")
            path = content.get("path", "no path")
            shortcut = Shortcut(index, title, path)
            self.shortcuts_list.controls.append(shortcut)
        # add shortcut to array

    def add_shortcut(self, id=0, title="", path=""):
        print('add')
        pass


class Shortcut(ft.UserControl):

    actions_menu_active = False
    edit_mode = False

    def __init__(self, id, title, path):
        super().__init__()
        self.id = id
        self.title = title
        self.path = path

    def build(self):
        self.info_txt_id = ft.Text(self.id, style=ft.TextThemeStyle.LABEL_LARGE,
                                   color="White",)
        self.info_txt_title = ft.Text(self.title, style=ft.TextThemeStyle.TITLE_MEDIUM,
                                      color="White", expand=True)
        self.info_display = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
            controls=[
                self.info_txt_id,
                self.info_txt_title
            ]
        )

        # get_directory_dialog.current.on_result = self.get_location_path
        self.txt_field_id = ft.TextField(label="ID", value=self.id, border=ft.InputBorder.UNDERLINE, keyboard_type=ft.KeyboardType.NUMBER,
                                         max_length=1, col=3, text_align=ft.TextAlign.CENTER, dense=True)
        self.txt_field_title = ft.TextField(label="Title", value=self.title, border=ft.InputBorder.UNDERLINE,
                                            max_length=12, border_radius=24, col=8, dense=True)
        self.txt_path = ft.Text(
            str(self.path) if self.path else "no location", col=9)

        self.get_directory_dialog = ft.FilePicker(
            on_result=self.get_location_path)

        global main_page
        main_page.overlay.extend([self.get_directory_dialog])

        self.edit_shortcut_mode = ft.ResponsiveRow(
            visible=self.edit_mode,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                self.txt_field_id,
                self.txt_field_title,
                ft.IconButton(icon=ft.icons.FOLDER_OPEN,
                              on_click=self.get_directory_dialog.get_directory_path, col=3),
                self.txt_path,
                ft.TextButton("Cancel", col=5,
                              on_click=self.cancel),
                ft.FilledButton("Save", icon=ft.icons.SAVE, col=5,
                                on_click=self.save),
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

        self.alert_dialog = ft.AlertDialog(
            title=ft.Text("Acabar o alearta de erro e o select folder demasiado lento"))
        main_page.dialog = self.alert_dialog
        self.alert_dialog.open = True

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
                        self.edit_shortcut_mode,
                        self.actions
                    ]
                )
            )
        )

    def actions_menu_toggle(self, e):
        if not self.edit_mode:
            self.actions.visible = not self.actions_menu_active
            self.actions_menu_active = not self.actions_menu_active
            self.update()

    def edit(self):
        # make info and actions disappear
        self.info_display.visible = False
        self.actions.visible = False

        # enable edit mode
        self.edit_mode = True
        self.edit_shortcut_mode.visible = True

        self.update()

    def save(self, e):
        txt_field_id = str(self.txt_field_id.value)
        txt_field_title = self.txt_field_title.value
        txt_path = self.txt_path.value

        if txt_field_id.isdigit() and txt_field_id and txt_field_title and txt_path:

            self.id = txt_field_id
            self.title = txt_field_title
            self.path = txt_path

            self.info_txt_id.value = self.id
            self.info_txt_title.value = self.title

            # disable edit mode
            self.edit_mode = False
            self.edit_shortcut_mode.visible = False

            # make info and actions disappear
            self.info_display.visible = True
            self.actions.visible = True

            self.update()

        else:
            if not txt_field_id.isdigit():
                self.alert_dialog.title = ft.Text(
                    "ID must be numeric between 1-6")
                self.alert_dialog.open = True
            elif not (txt_field_id and txt_field_title and txt_path):
                self.alert_dialog.title = ft.Text("Fill empty camps")
                self.alert_dialog.open = True

    def cancel(self, e):
        self.txt_path.value = self.path

        # disable edit mode
        self.edit_mode = False
        self.edit_shortcut_mode.visible = False

        # make info and actions disappear
        self.info_display.visible = True
        self.actions.visible = True

        self.update()

    def get_location_path(self, e):
        if e.path:
            path = e.path
            self.txt_path.value = path
            self.update()

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
        # get actions
        actions = self.read_stored_action()

        # add actions to list
        for action in actions:

            # create a string where it joins the name of the action and their hotkey
            action_title = f'{action["action"]} ({action["hotkey"]})'.capitalize(
            )

            # make actions that affect the shortcuts visually diferent from real actions
            if action.get('type'):
                action_button = ft.OutlinedButton(
                    action_title, col={"xs": 6, "sm": 6, "md": 2}, on_click=self.read_action,)
            else:
                action_button = ft.FilledTonalButton(
                    action_title, col={"xs": 12, "sm": 6, "md": 2}, on_click=self.read_action,)

            self.action_list.controls.append(action_button)

    def read_action(self, e):
        # gets the hotkey (mouse clicked)
        hotkey = e.control.text[-2:-1]

        match hotkey:
            case "e":
                self.edit()
            case _:
                print("not valid hotkey")


def main(page: ft.Page):

    global main_page
    main_page = page

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
