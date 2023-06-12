import flet as ft
from pytube import YouTube


def main(page: ft.Page):
    page.title = "Auto-scrolling ListView"

    def download_yt_file(e):
        print(f'\n{url_input.value}')
        print('Downloading...')

        try:
            yt = YouTube(str(url_input.value), use_oauth=True,
                         allow_oauth_cache=True)
            print(yt.streams.filter(file_extension="mp4"))
            mp4files = yt.streams.filter(only_audio=True)
            print(mp4files)

        except e:
            print("connection error")
            print(e)

    url_input = ft.TextField()
    download_button = ft.ElevatedButton(
        text="Download", on_click=download_yt_file)

    link_input_row = ft.Row(
        controls=[
            url_input,
            download_button
        ]
    )

    def get_directory_result(e: ft.FilePickerResultEvent):
        directory_path.value = e.path if e.path else "Cancelled!"
        directory_path.update()

    directory_path = ft.Text("pick a save location")
    get_directory_dialog = ft.FilePicker(on_result=get_directory_result)
    open_directory = ft.IconButton(
        icon=ft.icons.FOLDER_OPEN, on_click=lambda _: get_directory_dialog.get_directory_path())
    save_file_row = ft.Row(
        controls=[
            open_directory,
            directory_path
        ]
    )

    page.overlay.append(get_directory_dialog)

    page.add(
        ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                link_input_row,
                save_file_row
            ]
        )
    )


ft.app(target=main)
