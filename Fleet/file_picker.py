import flet as ft

dlg = ft.AlertDialog()

class test_layout(ft.UserControl):

    def build(self):

        dlg = ft.AlertDialog(
        title=ft.Text("Hello, you!"), on_dismiss=lambda e: print("Dialog dismissed!"))

        def open_dlg(e):
            dlg.open = True
            self.update()

        

        return ft.ElevatedButton("Open dialog", on_click=open_dlg)

    def input_check(self, e):
        global dlg
        open_dlg1(e)
        # self.page.dialog = dlg
        # dlg.open = True
        self.update()

def open_dlg1(e):
    global dlg
    # page.dialog = dlg
    dlg.open = True
    # page.update()


def main(page: ft.Page):
    page.title = "AlertDialog examples"

    global dlg
    dlg = ft.AlertDialog(
        title=ft.Text("Hello, you!"), on_dismiss=lambda e: print("Dialog dismissed!")
    )

    layout = test_layout()

    page.add(layout)

ft.app(target=main)