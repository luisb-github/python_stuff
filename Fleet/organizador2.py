from math import pi
import flet as ft
import json
import keyboard

dialog_result = ""
current_shortcuts = []
combination = "0"
listen_keyboard_events = True


class ShortcutsView(ft.UserControl):

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
        self.load_stored_shortcuts()

        return ft.Column(
            spacing=34,
            controls=[
                self.banner,
                self.shortcuts_list,
            ]
        )

    def read_stored_shortcuts(self):
        # decrypt file

        # opening json file
        json_file = open('organizador_data.json')

        # get shortcuts from json file
        json_data = json.load(json_file)
        stored_shortcuts = json_data.get("shortcuts", "")

        return stored_shortcuts

    def load_stored_shortcuts(self):
        # grab list of shortcuts
        stored_shortcuts = self.read_stored_shortcuts()

        # check if there is stored shortcuts
        if not stored_shortcuts:
            no_shortctuts_text = ft.Text("No shortcuts created", expand=True,
                                         text_align=ft.TextAlign.CENTER, style=ft.TextThemeStyle.LABEL_LARGE, )
            self.shortcuts_list.controls.append(no_shortctuts_text)
            return

        # append shortcuts to list
        for shortcut in stored_shortcuts:
            title = shortcut.get("title", "no title")
            path = shortcut.get("path", "no path")
            id = shortcut.get("id", "no id")
            shortcut = Shortcut(id, title, path, self.delete_shortcut)

            self.shortcuts_list.controls.append(shortcut)

            # add created shortcut to global array of current shortcuts
            global current_shortcuts
            current_shortcuts.append(shortcut)

    def add_shortcut(self, id=0, title="", path=""):
        global current_shortcuts
        id = len(current_shortcuts) + 1
        new_shortcut = Shortcut(id, title, path, self.delete_shortcut)
        current_shortcuts.append(new_shortcut)
        self.shortcuts_list.controls.append(new_shortcut)
        self.update()
        new_shortcut.edit()

    def delete_shortcut(self, shortcut):
        self.shortcuts_list.controls.remove(shortcut)

        self.update()


class Shortcut(ft.UserControl):

    actions_menu_active = False
    edit_mode = False

    def __init__(self, id, title, path, shortcut_delete):
        super().__init__()
        self.id = id
        self.title = title
        self.path = path
        self.shortcut_delete = shortcut_delete

    def build(self):
        self.info_txt_id = ft.Text(self.id, style=ft.TextThemeStyle.LABEL_LARGE,
                                   color="White",)
        self.info_txt_title = ft.Text(self.title, style=ft.TextThemeStyle.TITLE_MEDIUM,
                                      color="White", expand=True, )

        self.dropdown_toggle = ft.Icon(name=ft.icons.ARROW_DROP_DOWN_ROUNDED, )
        self.info_display = ft.Container(content=ft.Row(
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
            controls=[
                self.info_txt_id,
                self.info_txt_title,
                self.dropdown_toggle
            ]
        ), on_click=self.actions_menu_toggle)

        # get_directory_dialog.current.on_result = self.get_location_path
        self.txt_field_id = ft.TextField(label="ID", value=self.id, border=ft.InputBorder.UNDERLINE, keyboard_type=ft.KeyboardType.NUMBER,
                                         max_length=1, col=3, text_align=ft.TextAlign.CENTER, dense=True)
        self.txt_field_title = ft.TextField(label="Title", value=self.title, border=ft.InputBorder.UNDERLINE,
                                            max_length=12, border_radius=24, col=8, dense=True,)
        self.txt_path = ft.Text(
            str(self.path) if self.path else "no location", col=9)

        self.edit_shortcut_mode = ft.ResponsiveRow(
            visible=self.edit_mode,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                self.txt_field_id,
                self.txt_field_title,
                ft.IconButton(icon=ft.icons.FOLDER_OPEN,
                              on_click=self.change_shortcut_path, col=3),
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

        return ft.Card(
            expand=True,
            content=ft.Container(
                padding=ft.padding.symmetric(vertical=20, horizontal=20),
                border_radius=12,
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

    def actions_menu_toggle(self, e=""):
        if not self.edit_mode:
            self.actions.visible = not self.actions_menu_active
            self.actions_menu_active = not self.actions_menu_active
            self.dropdown_toggle.rotate = ft.Rotate(
                angle=0.0*pi, alignment=ft.alignment.center) if not self.actions_menu_active else ft.Rotate(
                angle=1.0*pi, alignment=ft.alignment.center)
            self.update()

    def set_keyboard_event_listen(self, state):
        global listen_keyboard_events
        listen_keyboard_events = state

    def edit(self):
        global listen_keyboard_events
        # make info and actions disappear
        self.info_display.visible = False
        self.actions.visible = False

        # enable edit mode
        self.edit_mode = True
        self.edit_shortcut_mode.visible = True

        self.set_keyboard_event_listen(False)

        self.update()

    def save(self, e):
        txt_field_id = str(self.txt_field_id.value)
        txt_field_title = self.txt_field_title.value
        txt_path = self.txt_path.value

        if txt_field_id.isdigit() and txt_field_id and txt_field_title and not txt_path in ["", " ", "no location", "No location"]:

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

        else:
            if not txt_field_id.isdigit():
                # self.lol_alert_dialog.title = ft.Text(
                #     "ID must be numeric between 1-6")
                pass
            else:
                # self.lol_alert_dialog.title = ft.Text("Fill empty camps")
                pass

            # self.lol_alert_dialog.open = True

        self.set_keyboard_event_listen(True)

        self.update()

    def cancel(self, e):
        # when new shortcut path and title empty -> so when cancel it disappears
        if not (self.path and self.title):
            self.delete()
            return

        self.txt_path.value = self.path

        # disable edit mode
        self.edit_mode = False
        self.edit_shortcut_mode.visible = False

        # make info and actions disappear
        self.info_display.visible = True
        self.actions.visible = True

        # remove action from combination
        global combination
        combination = combination[:-1]

        self.set_keyboard_event_listen(True)

        self.update()

    def change_shortcut_path(self, e):
        global dialog_result
        old_directory_path = dialog_result

        # open dialog
        get_directory_dialog.get_directory_path("Pick a location")

        while dialog_result == old_directory_path:
            pass

        self.txt_path.value = dialog_result
        self.update()

    def delete(self):
        global current_shortcuts

        shortcut_list_index = current_shortcuts.index(self)
        current_shortcuts.pop(shortcut_list_index)

        self.shortcut_delete(self)

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
                    action_title, col={"xs": 6, "sm": 6, "md": 2}, on_click=self.action_click,)
            else:
                action_button = ft.FilledTonalButton(
                    action_title, col={"xs": 12, "sm": 6, "md": 2}, on_click=self.action_click,)

            self.action_list.controls.append(action_button)

    def action_click(self, e):
        # gets the hotkey (mouse clicked)
        hotkey = e.control.text[-2:-1]

        self.read_action(hotkey)

    def read_action(self, action):
        match action:
            case "e":
                self.edit()

            case "d":
                self.delete()

            case _:
                print("not valid hotkey")


# get directory dialog result


def get_directory(e: ft.FilePickerResultEvent):
    global dialog_result
    dialog_result = e.path if e.path else "No location"


def main(page: ft.Page):

    global main_page
    main_page = page
    app_visibility = True
    active_current_shortcut_index = 0

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
    page.window_visible = app_visibility
    page.window_always_on_top = True

    def toggle_app():
        nonlocal app_visibility
        page.window_visible = not app_visibility
        app_visibility = not app_visibility
        page.window_focused = not app_visibility
        page.update()

    # file dialog
    global get_directory_dialog
    get_directory_dialog = ft.FilePicker(on_result=get_directory)

    page.dialog = get_directory_dialog
    page.overlay.append(get_directory_dialog)

    # open app on shortcut
    keyboard.add_hotkey('alt+shift+q', toggle_app,
                        suppress=True)

    # window event
    def window_event(e):
        nonlocal app_visibility

        if e.data in ['focus', 'restore']:
            pass
        if e.data in ['blur', 'minimized']:
            app_visibility = False
            page.window_visible = app_visibility

        page.update()

    # page.on_window_event = window_event

    # keyboard event

    def process_combination(hotkey):
        global combination
        nonlocal active_current_shortcut_index

        # listen to add events
        # make combination global and add on click
        # add a hoverbutton that with combination
        # backspace deletes one round
        # make and input for combinations for even more advanced users

        # logic problem to progress to second round *done*
        # keyboard listening while typing on edit is a problem *done*
        # disabled hide on losing focus
        # logic if i 1d and then e and then delete he will delete 2 because 2 now is in index 1
        print(hotkey)
        if hotkey in ['backspace', 'escape']:
            if hotkey == 'backspace':
                combination = combination[:-1]
            else:
                combination = "0"
                print("reset")

        # if hotkey is the same type as last combination digit swap with last digit
        elif (combination[-1].isdigit() and hotkey[-1].isdigit()) or (combination[-1].isalpha() and hotkey.isalpha()):
            combination = combination[:-1] + hotkey
        else:
            combination += hotkey

        print(combination)
        round = len(combination)
        match round:
            case 1:
                for shortcut in current_shortcuts:
                    if str(shortcut.id) == str(combination):
                        index = current_shortcuts.index(shortcut)
                        current_shortcuts[index].actions_menu_toggle()

                        active_current_shortcut_index = index
                        break
            case 2:
                action = combination[-1]
                index = active_current_shortcut_index
                current_shortcuts[index].read_action(
                    action)

    def keyboard_event(e):

        if not listen_keyboard_events:
            return

        key = str(e.key).lower()
        print(key)

        # enable numpad numbers
        if "numpad" in key:
            numpad_key = key.split()[-1]
            key = numpad_key if numpad_key.isdigit() else ""

        # filter: not empty, 1 character, digit or letter, special characters not filteres by alpha
        if key and len(key) == 1 and (key.isdigit() or key.isalpha()) and not key in ["º", "ª"]:
            process_combination(key)

        if key in ['backspace', 'escape']:
            process_combination(key)

    page.on_keyboard_event = keyboard_event
    # create application instance
    shortcut_view = ShortcutsView()

    # add application's root control to the page
    page.add(shortcut_view)
    page.update()


ft.app(target=main)
