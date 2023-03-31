import pyautogui
from PIL import ImageGrab, ImageFilter
import base64
from io import BytesIO


def blur_bg(x, y, width, height):

    # obter tamanho do ecra
    screen_width, screen_height = pyautogui.size()

    # descobrir onde esta posicionada e o seu tamanho a janela
    window_position_x = x
    window_position_y = y
    window_width = width
    window_height = height

    # tirar print

    bg_screenshot = ImageGrab.grab()

    # recortar essa parte da imagem
    img = bg_screenshot
    left = window_position_x
    top = window_position_y
    right = window_position_x + window_width
    bottom = window_position_y + window_height

    img_cropped = img.crop((left, top, right, bottom))

    # aplicar blur na img
    blur_img = img_cropped.filter(ImageFilter.GaussianBlur(10))

    # enviar resultado em base 64
    buffered = BytesIO()
    blur_img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str.decode('utf-8')
