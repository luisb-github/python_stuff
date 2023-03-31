import time
import win32gui
import win32process
import win32api
import keyboard
import win32con
import os
import shutil
from ahk import AHK
from ahk.directives import NoTrayIcon


ahk = AHK(directives=[NoTrayIcon])


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


def change_to_path(path):
    # send the hotkey to activate the address bar
    ahk.send_input("^l")
    time.sleep(0.05)
    ahk.send_input("^a")
    # ahk.send_input("{del}")
    keyboard.write(path + '\n')


def open_on_path(path):
    os.system(f"explorer {path}")


def go_to_path(path):
    is_explorer_window = check_is_explorer_window()
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


def main():
    keyboard.add_hotkey('ctrl+alt+shift+o', go_to_path,
                        args=['C:\\Users\\luisb\\Music\\vamosver\\'])
    keyboard.add_hotkey('ctrl+alt+shift+ç', go_to_path,
                        args=['C:\\Users\\luisb\\Documents\\'])
    keyboard.add_hotkey('ctrl+alt+shift+ç+m', move_to_path,
                        args=['C:\\Users\\luisb\\Documents\\'])
    keyboard.wait()


if __name__ == "__main__":
    main()
