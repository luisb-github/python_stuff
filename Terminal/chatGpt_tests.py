import pyautogui
import time


def get_address():
    TW = pyautogui.hotkey('ctrl', 'g')
    address = TW[10:]
    initial_ad = address[1:3]
    if initial_ad != ':\\':
        address = f"C:\\ESD"
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.05)
    pyautogui.typewrite(address)


def location():
    location = "C:\\ESD"
    pyautogui.click(button='left')
    pyautogui.typewrite(location + '\n')


if __name__ == '__main__':
    while True:
        key = pyautogui.hotkey('ctrl', 'g')
        if key == 'ctrl+g':
            get_address()
        elif key == 'ctrl+ç':
            location()
        else:
            break
