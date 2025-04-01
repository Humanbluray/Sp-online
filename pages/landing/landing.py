import flet as ft
from utils.styles import login_style
from utils.constantes import MAIN_COLOR, SECONDARY_COLOR
from utils import ElevBt, TextBt
from translations import translations, lang


class Connexion(ft.View):
    def __init__(self, page: object):
        super().__init__(
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            route="/", bgcolor="#f0f0f6",
        )
        self.page = page
        self.login = ft.TextField(
            **login_style, prefix_icon=ft.icons.ACCOUNT_CIRCLE_OUTLINED, label="Login",
        )
        self.passw = ft.TextField(
            **login_style, password=True, can_reveal_password=True, label=translations[lang]["password"],
            prefix_icon=ft.icons.KEY_OUTLINED
        )
        self.connect_bt = ElevBt(f"{translations[lang]["sign in"]}", MAIN_COLOR, None, self.connecter)
        self.new_account_bt = TextBt(f"{translations[lang]["sign up"]}", None)
        self.card = ft.Card(
            surface_tint_color="white", clip_behavior=ft.ClipBehavior.HARD_EDGE,
            elevation=10,
            content=ft.Container(
                padding=ft.padding.only(20, 30, 20, 30),
                bgcolor='white', border_radius=16, width=260,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text("School", size=32, font_family="PPB", color=MAIN_COLOR),
                                ft.Text("Pilot", size=32, font_family="PPB", color=SECONDARY_COLOR),
                            ], spacing=0, alignment=ft.MainAxisAlignment.CENTER
                        ),
                        ft.Divider(height=1, color=ft.Colors.TRANSPARENT),
                        ft.Text(f"{translations[lang]["enter informations"]}", color="black", size=16, font_family="QSM"),
                        self.login, self.passw,
                        ft.Divider(height=1, color=ft.Colors.TRANSPARENT),
                        self.connect_bt,
                        self.new_account_bt
                    ]
                )
            )
        )
        self.controls=[
            ft.Stack(
                controls=[
                    self.card
                ]
            )
        ]

    def connecter(self, e):
        self.page.go('/accueil')

