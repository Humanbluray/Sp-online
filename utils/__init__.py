import flet as ft

from utils.constantes import *


class ElevBt(ft.ElevatedButton):
    def __init__(self, texte: str, couleur: str, length, click):
        super().__init__(
            on_hover=self.hover_effect, on_click=click, scale=ft.transform.Scale(1),
            animate_scale=ft.animation.Animation(300, ft.AnimationCurve.EASE),
            bgcolor=couleur, height=45, width=length,
            style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=24)),
            content=ft.Row(
                controls=[
                    ft.Text(texte.capitalize(), size=13, font_family="PPB", color="white")
                ], spacing=5, alignment=ft.MainAxisAlignment.CENTER
            )
        )

    def hover_effect(self, e):
        if e.data == "true":
            self.scale = 1.05
            self.update()
        else:
            self.scale = 1
            self.update()


class TextBt(ft.TextButton):
    def __init__(self, texte: str, click):
        super().__init__(
            on_hover=self.hover_effect, on_click=click, scale=ft.transform.Scale(1),
            animate_scale=ft.animation.Animation(300, ft.AnimationCurve.EASE),
            content=ft.Row(
                controls=[
                    ft.Text(texte.capitalize(), size=12, font_family="PPM",color=MAIN_COLOR)
                ], alignment=ft.MainAxisAlignment.CENTER
            )
        )

    def hover_effect(self, e):
        if e.data == "true":
            self.scale = 1.05
            self.update()
        else:
            self.scale = 1
            self.update()


class FloatBt(ft.FloatingActionButton):
    def __init__(self, click):
        super().__init__(
            bgcolor=MAIN_COLOR, scale=0.8,
            content=ft.Row(
                controls=[ft.Icon(ft.icons.ADD, color="white", size=24)],
                alignment=ft.MainAxisAlignment.CENTER,
            ), on_click=click, opacity=0.8
        )


class CtButton(ft.Container):
    def __init__(self, icone, click):
        super().__init__(
            border=ft.border.all(1, "grey"),
            border_radius=6, bgcolor="#f0f0f6", padding=5,
            on_click=click,
            scale=ft.transform.Scale(1),
            animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_OUT_SLOWIN),
            on_hover=self.icon_bt_hover,
            tooltip="Supprimer filtres",
        )
        self.content = ft.Icon(icone, color=ft.colors.BLACK45)

    @staticmethod
    def icon_bt_hover(e):
        if e.data == 'true':
            e.control.scale = 1.2
            e.control.content.color = "black"
            e.control.content.update()
            e.control.update()
        else:
            e.control.scale = 1
            e.control.content.color = "black45"
            e.control.content.update()
            e.control.update()

