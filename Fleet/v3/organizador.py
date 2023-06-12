import flet as ft
import winreg


def get_accent_color():
    registry_key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\DWM")
    value, regtype = winreg.QueryValueEx(registry_key, "ColorizationColor")
    winreg.CloseKey(registry_key)

    # The value is in decimal format, convert it to hex
    value_hex = format(value, 'x')

    # The color is in BGR format and the opacity is also included.
    # We need to convert it to RGB format and exclude the opacity.
    bgr = value_hex[2:]  # Exclude opacity
    b, g, r = bgr[4:], bgr[2:4], bgr[:2]  # BGR to RGB
    rgb = r + g + b

    return '#' + rgb


def main(page: ft.Page):

    windows_accent_color = get_accent_color()

    page.title = "Organizador"

    # window theme
    page.theme = page.dark_theme = ft.theme.Theme(
        color_scheme_seed=windows_accent_color,
        use_material3=True,
        visual_density=ft.ThemeVisualDensity.ADAPTIVEPLATFORMDENSITY
    )
    page.theme_mode = ft.ThemeMode.SYSTEM

    # window size & position
    page.window_width = 600
    page.window_height = 700
    page.window_top = 600
    page.window_left = 1800

    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.TextField(
        value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                txt_number,
                ft.IconButton(ft.icons.ADD, on_click=plus_click),
                ft.ElevatedButton("click Me")
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


ft.app(target=main)
