import flet as ft
from utils.constantes import *


class TopMenu(ft.Card):
    def __init__(self, cp):
        super().__init__(
            elevation=1, surface_tint_color="white",
        )
        self.cp = cp
        self.content = ft.Container(
            padding=10, bgcolor="white",
            content=ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.IconButton(ft.Icons.MENU, icon_size=20, icon_color=ft.Colors.BLACK54),
                            ft.Row(
                                controls=[
                                    ft.Text("School", size=22, font_family="PPB", color=MAIN_COLOR),
                                    ft.Text("Pilot", size=22, font_family="PPB", color=SECONDARY_COLOR),
                                ], spacing=0, alignment=ft.MainAxisAlignment.CENTER
                            ),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            ft.Container(
                                shape=ft.BoxShape.CIRCLE, width=35, height=35, bgcolor="#f0f0f6",
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(ft.icons.SETTINGS, color="black")
                                    ], alignment=ft.MainAxisAlignment.CENTER
                                )
                            ),
                            ft.PopupMenuButton(
                                content=ft.CircleAvatar(
                                    content=ft.Text("A", size=18, font_family="PPB"),  # Remplace "A" par ton avatar réel
                                    radius=20
                                ),
                                items=[
                                    ft.PopupMenuItem(
                                        content=ft.Row(
                                            controls=[
                                                ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.BLACK38,
                                                        size=18),
                                                ft.Text("Deconnexion".upper(), size=13, font_family="PPM",
                                                        color=ft.Colors.BLACK87)
                                            ], alignment=ft.MainAxisAlignment.START
                                        )
                                    ),

                                ]
                            )
                        ]
                    )

                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )