#! maneira de dar upload de cenas copiadas nos browsers (não tem a ver com este projeto)
import os
import shutil
import time
import flet as ft
import keyboard
import win32api
import win32con
import win32gui 
import win32process
from ahk import AHK
from ahk.directives import NoTrayIcon

ahk = AHK(directives=[NoTrayIcon])

window_minimized = False

# vars for Logic
shortcuts = [
    {"name": "Documents", "path": "Documents"},
    {"name": "Vamos Ver", "path": "C:\\Users\\luisb\\Music\\vamosver"},
]

actions = [
    {"action": "open", "hotkey": "o"},
    {"action": "change to", "hotkey": "c"},
    {"action": "move to", "hotkey": "m"},
    {"action": "edit location", "hotkey": "e", "type": "edition"},
    {"action": "delete", "hotkey": "d", "type": "edition"},
]

program_hotkey = 'alt+shift+q'


def main(page: ft.Page):
    # window settings
    window_position_x = 2100
    window_position_y = 700
    window_width = 350
    window_height = 700

    # vars for GUI
    bt_add_shortcut = ft.Ref[ft.IconButton]()
    bt_settings = ft.Ref[ft.IconButton]()
    list_shortcuts = ft.Ref[ft.ListView]()
    hwnd = win32gui.FindWindow(None, "organizador")
    step = 1

    # page.window_left = window_position_x
    # page.window_top = window_position_y
    page.window_width = window_width
    page.window_height = window_height
    page.padding = 20
    page.window_resizable = False
    page.title = "organizador"
    page.window_visible = True
    page.window_always_on_top = True

    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)

    def load_list_shortcuts():
        for index, content in enumerate(shortcuts, 1):
            list_shortcuts.current.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(
                                    f'{index}', style=ft.TextThemeStyle.LABEL_LARGE, color="White",),
                                ft.Text(f'{content["name"]}',
                                        style=ft.TextThemeStyle.TITLE_MEDIUM, color="White", expand=True),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                            spacing=20
                        ),
                        height=80,
                        expand=True,
                        padding=20,
                        border_radius=12,
                        ink=True,
                        on_click=lambda e: print(
                            "Clickable transparent with Ink clicked!"),
                    ),
                    expand=True,
                    elevation=1.5
                )
            )

    def window_event(e):
        global window_minimized
        hwnd = win32gui.FindWindow(None, "organizador")

        if e.data in ['focus', 'restore']:
            window_minimized = False
        if e.data in ['blur', 'minimized']:
            window_minimized = True

    def keyboard_event(e):
        hotkey_string = keyboard_event_to_string(
            e.ctrl, e.alt, e.shift, e.meta, e.key)
        print(hotkey_string)

    def keyboard_event_to_string(ctrl, alt, shift, meta, key):
        hotkey_string = ""
        print(ctrl, alt, shift, meta, key)
        if ctrl:
            hotkey_string += "ctrl" if not hotkey_string else "+ctrl"
        if alt:
            hotkey_string += "alt" if not hotkey_string else "+alt"
        if shift:
            hotkey_string += "shift" if not hotkey_string else "+shift"
        if meta:
            hotkey_string += "windows" if not hotkey_string else "+windows"

        hotkey_string += f'{key}' if not hotkey_string else f'+{key}'

        print(hotkey_string)
        return hotkey_string

    def activity(hotkey):

        if step == 1:
            match hotkey:
                case 1:
                    print('1')

        if step == 2:
            match hotkey:
                case 'o':
                    print('o')
                case 'c':
                    print('o')

    def toggle_app():
        global window_minimized

        hwnd = win32gui.FindWindow(None, "organizador")
        print(window_minimized)
        if window_minimized:
            show_app(hwnd)
        else:
            hide_app(hwnd)

    def show_app(hwnd):
        print('show')
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNOACTIVATE)

    def hide_app(hwnd):
        print('hide')
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

    page.add(ft.Row([
        ft.IconButton(ref=bt_add_shortcut, icon=ft.icons.ADD,
                      icon_color="white", icon_size=22, tooltip="Add shortcut",),
        ft.IconButton(ref=bt_settings, icon=ft.icons.SETTINGS,
                      icon_color="white", icon_size=22, tooltip="Settings",)
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Row([
            ft.ListView(ref=list_shortcuts, expand=True,
                        spacing=14,)
        ]))

    load_list_shortcuts()

    # keyboard.add_hotkey(program_hotkey, toggle_app,
    #                     suppress=True)

    page.on_window_event = window_event
    page.on_keyboard_event = keyboard_event

    page.update()


def check_is_explorer_window():
    # Get handle to focused window
    focused_window = win32gui.GetForegroundWindow()

    # Get process id and executable name of the focused window
    pid = win32process.GetWindowThreadProcessId(focused_window)[1]
    process_handle = win32api.OpenProcess(
        win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid)

    executable = win32process.GetModuleFileNameEx(process_handle, 0)

    if not process_handle:
        return []

    # Check if the focused window is a Windows File Explorer process
    if "explorer.exe" in executable.lower():
        return True
    else:
        return False


def path_of_id(id):
    if not len(shortcuts.keys()) < int(id):
        return shortcuts[id]['path']

    return None


def change_to_path(path):
    # send the hotkey to activate the address bar
    ahk.send_input("^l")
    time.sleep(0.05)
    ahk.send_input("^a")
    # ahk.send_input("{del}")
    keyboard.write(path + '\n')


def open_on_path(path):
    os.system(f"explorer {path}")


def go_to_path(id):
    print('go to path')
    is_explorer_window = check_is_explorer_window()
    path = path_of_id(str(id))
    if is_explorer_window:
        change_to_path(path)

    else:
        open_on_path(path)


def move_to_path(path):

    # ahk.send_input("^c")
    # result = ahk.run_script("move.ahk")
    # print(result)
    files_to_move = ""
    files_to_move = ahk.run_script(
        'Clipboard= \n SendInput, ^c  \n ClipWait \n file_paths := Clipboard \n FileAppend, %file_paths%, *, UTF-8 \n ExitApp').replace('\r', '').strip().split('\n')

    print(files_to_move)

    for file in files_to_move:
        file_name = os.path.basename(file)
        print(file)
        destination = str(path) + str(file_name)

        shutil.move(file, destination)


ft.app(target=main)
