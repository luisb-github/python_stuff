import flet as ft


class Card(ft.ElevatedButton):
    def __init__(self, number):

        super().__init__(
            text=str(number),
            on_click=self.show_alert
        )

        self.number = number

    def show_alert(self, e):
        alert_dialog = ft.AlertDialog(
            title=ft.Text("Number Alert"),
            content=ft.Text(f"You clicked: {self.number}"),
        )
        e.page.dialog = alert_dialog
        alert_dialog.open = True
        e.page.update()


def main(page: ft.Page):
    page.title = "Numbered Cards"

    # Create 10 cards with numbers 1-10
    for i in range(1, 11):
        page.add(Card(i))


ft.app(target=main)
