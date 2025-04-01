import flet as ft
from utils.constantes import SECONDARY_COLOR, MAIN_COLOR, TERTIARY_COLOR
from backend.be_eleves import running_year
from pages.accueil.onglets.eleves import Eleves
from translations import translations, lang


class ItemMenu(ft.Container):
    def __init__(self, title: str, my_icon: str, selected_icon_color: str, selected_text_color: str):
        super(ItemMenu, self).__init__(
            on_hover=self.hover_ct,
            shape=ft.BoxShape.RECTANGLE,
            padding=ft.padding.only(10, 9, 0, 9),
            border_radius=14,
            scale=ft.transform.Scale(1),
            animate_scale=ft.animation.Animation(300, ft.AnimationCurve.FAST_LINEAR_TO_SLOW_EASE_IN)
        )
        self.title = title
        self.my_icon = my_icon
        self.is_clicked = False
        self.selected_icon_color = selected_icon_color
        self.selected_text_color = selected_text_color

        self.visuel = ft.Icon(my_icon, size=18, color=selected_icon_color)
        self.name = ft.Text(title, size=12, font_family="PPM", color=selected_text_color)

        self.content = ft.Row(controls=[self.visuel, self.name], alignment=ft.MainAxisAlignment.START)

    def hover_ct(self, e):
        if e.data == "true":
            e.control.scale = 1.15
            e.control.update()
        else:
            if self.is_clicked:
                self.visuel.color = TERTIARY_COLOR
                self.name.font_family = "PPB"
                self.name.size = 13
                self.name.color = MAIN_COLOR
                self.bgcolor = "#f0f0f6"
                self.visuel.update()
                self.name.update()
                self.update()
            else:
                self.visuel.color = self.selected_icon_color
                self.name.font_family = "PPM"
                self.name.size = 12
                self.name.color = self.selected_text_color
                self.bgcolor = None
                self.visuel.update()
                self.name.update()
                self.update()

            e.control.scale = 1
            e.control.update()

    def set_is_clicked_true(self):
        self.is_clicked = True
        self.visuel.color = TERTIARY_COLOR
        self.name.font_family = "PPB"
        self.name.size = 13
        self.name.color = MAIN_COLOR
        self.bgcolor = "#f0f0f6"
        self.visuel.update()
        self.name.update()
        self.update()

    def set_is_clicked_false(self):
        self.is_clicked = False
        self.visuel.color = self.selected_icon_color
        self.name.font_family = "PPM"
        self.name.size = 12
        self.name.color = self.selected_text_color
        self.bgcolor = None
        self.visuel.update()
        self.name.update()
        self.update()


class Menu(ft.Container):
    def __init__(self, cp: object):
        super(Menu, self).__init__(
            bgcolor="white",
            padding=ft.padding.only(20, 15, 20, 15),
            border_radius=0,
        )
        self.cp = cp  # Conteneur parent
        color_icon = ft.Colors.BLACK38
        color_text = ft.Colors.BLACK87

        self.eleves = ItemMenu(translations[lang]["students_menu"].upper(), ft.icons.PERSON_OUTLINED, color_icon, color_text)
        self.timetable = ItemMenu(translations[lang]["time_menu"].upper(), ft.icons.FILTER_TILT_SHIFT_OUTLINED, color_icon, color_text)
        self.classes = ItemMenu(translations[lang]["classes_menu"].upper(), ft.icons.ACCOUNT_BALANCE_OUTLINED, color_icon, color_text)
        self.professeurs = ItemMenu(translations[lang]["teachers_menu"].upper(), ft.icons.GROUP_OUTLINED, color_icon, color_text)
        self.pensions = ItemMenu(translations[lang]["school_fees_menu"].upper(), ft.icons.MONETIZATION_ON_OUTLINED, color_icon, color_text)
        self.notes= ItemMenu(translations[lang]["notes_menu"].upper(), ft.icons.NOTES_OUTLINED, color_icon, color_text)
        self.bull = ItemMenu(translations[lang]["bull_menu"].upper(), ft.icons.SCHOOL_OUTLINED, color_icon, color_text)
        self.users = ItemMenu(translations[lang]["users_menu"].upper(), ft.icons.GROUPS_OUTLINED, color_icon, color_text)
        self.annees = ItemMenu(translations[lang]["annees_menu"].upper(), ft.icons.EDIT_CALENDAR_OUTLINED, color_icon, color_text)

        self.children = [
            self.eleves, self.timetable, self.classes, self.professeurs,
            self.pensions, self.notes, self.bull, self.annees, self.users,
        ]

        for item in self.children:
            item.on_click = self.cliquer_menu

        self.content = ft.Column(
            controls=[
                ft.Column(
                    controls=[
                        ft.Divider(height=2, color="transparent"),
                        ft.Column(
                            controls=[
                                self.eleves, self.classes, self.professeurs, self.timetable,
                                self.pensions, self.notes, self.bull, self.users,
                                self.annees
                            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                    ]
                ),
                ft.Column(
                    controls=[
                        ft.Divider(height=1, thickness=1),
                        ft.Column(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            translations[lang]["current year"].upper(),
                                            size=11, font_family="PPM"),
                                        ft.Text(
                                            f"{running_year()} - {int(running_year()) + 1}",
                                            size=11, font_family="PPM"),
                                    ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                ),
                                ft.Text("SCHOOL PILOT V1.0", size=10),
                            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=30,
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

    def cliquer_menu(self, e):
        for item in self.children:
            item.set_is_clicked_false()

        e.control.set_is_clicked_true()
        e.control.update()

        for row in self.cp.contenu.content.controls[:]:
            self.cp.contenu.content.controls.remove(row)

        if e.control.name.value == translations[lang]["students_menu"].upper():
            self.cp.contenu.content.controls.append(Eleves(self.cp))
            self.cp.update()

