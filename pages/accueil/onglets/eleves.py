import json
import os.path

import fontTools.ttLib.tables.C_P_A_L_

from utils.useful_functions import ajout_separateur_virgule
from utils import FloatBt, ElevBt, CtButton
from utils.components import FicheEleve
from utils.styles import *
from utils import SECONDARY_COLOR
from backend.be_eleves import running_year
import datetime
from backend.be_eleves import *
import PIL
import mimetypes
from translations import translations, lang

DEFAULT_URL = "https://nppwkqytgqlqijpeulfj.supabase.co/storage/v1/object/public/students_pictures//silhouette.png"
BUCKET_NAME = "students_pictures"


class Eleves(ft.Container):
    def __init__(self, cp: object):
        super().__init__(
            padding=20, expand=True
        )
        self.cp = cp
        self.results = ft.Text("", size=14, font_family="PPB")
        self.bt_filtres = CtButton(ft.icons.FILTER_ALT_OUTLINED, self.filter_datas)
        self.bt_supp_filtres = CtButton(ft.icons.FILTER_ALT_OFF_OUTLINED, self.supp_filter)

        self.filtre_eleves = ft.TextField(**field_style, width=250, prefix_icon=ft.icons.FILTER_ALT_OUTLINED, label=translations[lang]["filter"])
        self.bt_new_elev = FloatBt(self.open_new_elv_frame)
        self.list = ft.ListView(expand=True, spacing=10, divider_thickness=1)

        # Nouvel élève .............................................................
        self.picture = None
        self.n_name = ft.TextField(**field_style_2, width=450, prefix_icon="person_outlined", label=translations[lang]["name"])
        self.n_surname = ft.TextField(**field_style_2, width=450, prefix_icon="person_outlined", label=translations[lang]["first name"])
        self.n_sel_date = ft.TextField(**date_field_style, label="AAAA-MM-JJ", width=160)
        self.cp.dp_new_eleve.on_change = self.change_date_new_elev
        self.bt_select_date = ft.IconButton(
            ft.icons.CALENDAR_MONTH_OUTLINED, scale=0.8, bgcolor="white",
            icon_color="black",
            on_click=lambda _: self.cp.page.open(self.cp.dp_new_eleve), right=3
        )
        self.n_lieu = ft.TextField(**field_style_2, width=250, prefix_icon=ft.icons.LOCATION_ON_OUTLINED,
                                   label=translations[lang]["born in"])
        self.sexe = ft.RadioGroup(
            content=ft.Row(
                controls=[
                    ft.Radio(**radio_style, label=translations[lang]['female'], value="F"),
                    ft.Radio(**radio_style, label=translations[lang]['male'], value="M"),
                ],
            )
        )
        self.n_pere = ft.TextField(**field_style_2, width=400, prefix_icon=ft.icons.MAN_OUTLINED, label=translations[lang]["father"])
        self.n_mere = ft.TextField(**field_style_2, width=400, prefix_icon=ft.icons.WOMAN_OUTLINED,
                                   label=translations[lang]["mother"])
        self.n_contact = ft.TextField(
            **field_style_2, width=200, prefix_icon=ft.icons.PHONE_ANDROID, label=translations[lang]["contact"],
            text_align=ft.TextAlign.RIGHT,
            input_filter=ft.NumbersOnlyInputFilter()
        )
        self.n_autre = ft.TextField(
            **field_style_2, width=200, prefix_icon=ft.icons.PHONE_ANDROID, label=translations[lang]["contact 2"],
            text_align=ft.TextAlign.RIGHT,
            input_filter=ft.NumbersOnlyInputFilter()
        )
        self.n_class = ft.Dropdown(
            **drop_style, prefix_icon=ft.icons.ACCOUNT_BALANCE_OUTLINED, width=170, on_change=self.changement_classe_new,
            label=translations[lang]["class"], enable_search=True
        )
        self.n_mat = ft.TextField(
            **underline_field_style, prefix_icon=ft.icons.CREDIT_CARD_OUTLINED, width=250, label=translations[lang]["registration number"]
        )
        self.n_effectif = ft.TextField(
            **underline_field_style, prefix_icon=ft.icons.KEYBOARD_DOUBLE_ARROW_UP_OUTLINED, width=125,
            text_align=ft.TextAlign.RIGHT,
            label=translations[lang]["head count"]
        )
        self.n_check = ft.Checkbox(
            label=translations[lang]["repeater_ins"], label_style=ft.TextStyle(**text_title_style),
            active_color="#f0f0f6", check_color=SECONDARY_COLOR
        )
        self.n_frais = ft.TextField(
            **underline_field_style, prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED, width=150,
            text_align=ft.TextAlign.RIGHT,
            label=translations[lang]["fees"]
        )
        self.n_tranche_1 = ft.TextField(
            **field_style_2, width=150, label=translations[lang]["fees part 1"], input_filter=ft.NumbersOnlyInputFilter(),
            prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED,
            text_align=ft.TextAlign.RIGHT
        )
        self.n_tranche_2 = ft.TextField(
            **field_style_2, width=150, label=translations[lang]["fees part 2"], input_filter=ft.NumbersOnlyInputFilter(),
            prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED,
            text_align=ft.TextAlign.RIGHT
        )
        self.n_tranche_3 = ft.TextField(
            **field_style_2, width=150, label=translations[lang]["fees part 3"], input_filter=ft.NumbersOnlyInputFilter(),
            prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED,
            text_align=ft.TextAlign.RIGHT
        )
        self.n_switch = ft.Switch(
            active_color=ft.colors.GREY, thumb_color=SECONDARY_COLOR, track_outline_color="black",
            scale=0.7, on_change=self.changement_solde_new,
        )
        self.new_image_box = ft.Container(
            width=120, height=120, border_radius=12,
            bgcolor="#f0f06",
            content=ft.Image(src=DEFAULT_URL)
        )
        self.cp.fp_new_eleve.on_result = self.select_image

        self.new_elv_frame = ft.Card(
            elevation=50, surface_tint_color="white", width=700, height=600, expand=True,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                padding=10, bgcolor="white",
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Container(
                            padding=10, bgcolor="#f0f0f6", border_radius=12,
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.PERSON_ADD_OUTLINED, size=20, color="black"),
                                            ft.Text(translations[lang]["new student"].upper(), size=16, font_family="PPB",),
                                        ]
                                    ),
                                    ft.IconButton(
                                        'close', scale=0.7, icon_color="black", bgcolor="#f0f0f6",
                                        on_click=self.close_new_elv_frame,
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=10, bgcolor="white", border_radius=12, expand=True,
                            content=ft.Column(
                                expand=True, scroll=ft.ScrollMode.AUTO,
                                controls=[
                                    ft.Container(
                                        padding=10, content=ft.Column(
                                            controls=[
                                                ft.Column(
                                                    controls=[
                                                        ft.Text(translations[lang]["student data"].upper(), size=12, font_family="PPB", color=MAIN_COLOR),
                                                        ft.Divider(height=1, thickness=1),
                                                    ], spacing=0
                                                ),
                                                ft.Row(
                                                    controls=[
                                                        ft.Stack(
                                                            controls=[
                                                                self.new_image_box,
                                                                ft.IconButton(
                                                                    ft.icons.ADD_A_PHOTO_ROUNDED, icon_size=28, icon_color="black",
                                                                    bgcolor="#f0f0f6",
                                                                    on_click=lambda e: self.cp.fp_new_eleve.pick_files(
                                                                        allowed_extensions=['jpg', 'png', "webp", "avif"])
                                                                )
                                                            ], alignment=ft.alignment.bottom_right
                                                        ),
                                                        ft.Column(
                                                            controls=[
                                                                self.n_name,
                                                                self.n_surname,
                                                                ft.Row(
                                                                    controls=[
                                                                        ft.Stack(
                                                                            controls=[
                                                                                self.n_sel_date, self.bt_select_date,
                                                                            ], alignment=ft.alignment.center_right
                                                                        ),
                                                                        self.n_lieu,
                                                                    ]
                                                                ),
                                                                ft.Row(
                                                                    controls=[
                                                                        ft.Text(translations[lang]["gender"], size=12, font_family="PPM"),
                                                                        self.sexe,

                                                                    ], spacing=10
                                                                ),
                                                                ft.Row([self.n_autre, self.n_contact,]),
                                                                self.n_pere, self.n_mere,
                                                                ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                                                            ]
                                                        )
                                                    ], spacing=20,
                                                    vertical_alignment=ft.CrossAxisAlignment.START
                                                ),
                                                ft.Column(
                                                    controls=[
                                                        ft.Text(translations[lang]["register"].upper(), size=12,
                                                                font_family="PPB", color=MAIN_COLOR,
                                                                weight=ft.FontWeight.BOLD),
                                                        ft.Divider(height=1, thickness=1),
                                                    ], spacing=0
                                                ),
                                                ft.Row(
                                                    controls=[
                                                        ft.Text(translations[lang]["academic year"].upper(), size=12, font_family="PPM"),
                                                        ft.TextField(
                                                            **underline_field_style,
                                                            prefix_icon=ft.icons.EDIT_CALENDAR_OUTLINED,
                                                            width=90, value=running_year()
                                                        ),
                                                        ft.Row([self.n_class, self.n_effectif]),
                                                    ]
                                                ),
                                                ft.Row([self.n_mat, self.n_frais]),
                                                self.n_check,
                                                ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                                                ft.Column(
                                                    controls=[
                                                        ft.Text(translations[lang]["school fees"].upper(), size=12, font_family="PPB", color=MAIN_COLOR),
                                                        ft.Divider(height=1, thickness=1),
                                                    ], spacing=0
                                                ),
                                                ft.Row(
                                                    [
                                                        ft.Text(translations[lang]['pay off'].upper(), size=12,
                                                                font_family="PPM"),
                                                        self.n_switch
                                                    ]
                                                ),
                                                ft.Row(
                                                    controls=[
                                                        self.n_tranche_1, self.n_tranche_2, self.n_tranche_3
                                                    ]
                                                ),
                                                ElevBt(translations[lang]['valid'], MAIN_COLOR, 150, self.create_eleve)
                                            ], spacing=15
                                        )
                                    )
                                ], spacing=5
                            )
                        )
                    ], spacing=20
                )
            )
        )

        # fenetre de modification .............................
        self.edit_id = ft.TextField(**underline_field_style, width=90, label="id", visible=False)
        self.matricule = ft.TextField(**underline_field_style, width=250, label=translations[lang]["registration number"], suffix_icon=ft.icons.CREDIT_CARD)
        self.edit_nom = ft.TextField(**field_style_2, label=translations[lang]["name"], width=450, prefix_icon=ft.icons.PERSON_OUTLINED)
        self.edit_prenom = ft.TextField(**field_style_2, label=translations[lang]["first name"], width=450, prefix_icon=ft.icons.PERSON_OUTLINED)
        self.sel_date = ft.TextField(**date_field_style, label=translations[lang]["born in"], width=170)

        self.cp.dp_modif_eleve.on_change = self.change_date_edit_elev
        self.edit_bt_select_date = ft.IconButton(
            ft.icons.CALENDAR_MONTH_OUTLINED, scale=0.7, bgcolor="white",
            icon_color="black",
            on_click=lambda _: self.cp.page.open(self.cp.dp_modif_eleve)
        )
        self.edit_lieu = ft.TextField(**field_style_2, label=translations[lang]["born at"], width=180, prefix_icon=ft.icons.HOME_OUTLINED)
        self.edit_sexe = ft.TextField(**field_style_2, label=translations[lang]["gender"], width=120)
        self.edit_pere = ft.TextField(**field_style_2, width=450, label=translations[lang]['father'], prefix_icon="man_outlined")
        self.edit_mere = ft.TextField(**field_style_2, width=450, label=translations[lang]['mother'], prefix_icon="woman_outlined")
        self.edit_tel = ft.TextField(**field_style_2, width=200, label=translations[lang]['contact'], prefix_icon=ft.icons.PHONE_ANDROID_OUTLINED)
        self.edit_autre = ft.TextField(**field_style_2, width=200, label=translations[lang]['contact 2'], prefix_icon=ft.icons.PHONE_ANDROID_OUTLINED)
        self.edit_image_box = ft.Container(
            width=120, height=120, border_radius=12,
            bgcolor="#f0f06",
            content=ft.Image(src=DEFAULT_URL)
        )
        self.cp.fp_edit_eleve.on_result = self.select_edit_image
        self.edit_picture = None

        self.edit_elv_frame = ft.Card(
            elevation=50, surface_tint_color="white", variant=ft.CardVariant.ELEVATED,
            shadow_color=ft.Colors.BLACK,
            width=700, height=600, expand=True,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                padding=10, bgcolor="white", border_radius=16, border=ft.border.all(1, "#f0f0f6"),
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Container(
                            padding=10, bgcolor="#f0f0f6", border_radius=12,
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.EDIT_OUTLINED, size=20, color="black"),
                                            ft.Text(translations[lang]["edit student"].upper(), size=16, font_family="PPB", ),
                                        ]
                                    ),
                                    ft.IconButton(
                                        'close', scale=0.7, icon_color="black", bgcolor="#f0f0f6",
                                        on_click=self.close_edit_elv_frame,
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=10, bgcolor="white", border_radius=12, expand=True,
                            content=ft.Column(
                                controls=[
                                    ft.Row(
                                        expand=True, scroll=ft.ScrollMode.AUTO,
                                        controls=[
                                            ft.Column(
                                                controls=[
                                                    ft.Stack(
                                                        controls=[
                                                            self.edit_image_box,
                                                            ft.IconButton(
                                                                ft.Icons.ADD_A_PHOTO, icon_color="black", icon_size=20, bgcolor="#f0f0f6",
                                                                on_click=lambda e: self.cp.fp_edit_eleve.pick_files(
                                                                    allowed_extensions=['jpg', 'png', "webp", "avif"]
                                                                )
                                                            )
                                                        ], alignment=ft.alignment.bottom_right
                                                    ),
                                                    ElevBt(f"{translations[lang]['valid']}", MAIN_COLOR, 120, self.modifier_eleve)
                                                ]
                                            ),
                                            ft.VerticalDivider(width=10, thickness=1),
                                            ft.Column(
                                                expand=True, scroll=ft.ScrollMode.AUTO,
                                                spacing=15,
                                                controls=[
                                                    ft.Column(
                                                        controls=[
                                                            ft.Text(translations[lang]['student data'].upper(), size=10, font_family="PPB"),
                                                            ft.Divider(height=1, thickness=1)
                                                        ],
                                                        spacing=0
                                                    ),
                                                    self.edit_nom, self.edit_prenom,
                                                    ft.Row(
                                                        controls=[
                                                            self.edit_sexe,
                                                            ft.IconButton(
                                                                ft.icons.CHANGE_CIRCLE_OUTLINED,
                                                                icon_color=ft.Colors.BLACK45,
                                                                icon_size=24, on_click=self.changer_sexe
                                                            )
                                                        ]
                                                    ),
                                                    ft.Row(
                                                        controls=[
                                                            ft.Stack(
                                                                controls=[
                                                                    self.sel_date,
                                                                    self.edit_bt_select_date, ],
                                                                alignment=ft.alignment.center_right
                                                            ),
                                                            self.edit_lieu,
                                                        ]
                                                    ),
                                                    ft.Row([self.edit_tel, self.edit_autre,]),
                                                    self.edit_pere, self.edit_mere,
                                                    self.edit_id,
                                                ]
                                            )
                                        ]
                                    ),
                                ]
                            )
                        )
                    ], spacing=20
                )
            )
        )

        # inscription window ...
        self.ins_class = ft.Dropdown(
            **drop_style, prefix_icon=ft.icons.ACCOUNT_BALANCE_OUTLINED, width=170,
            on_change=self.changement_classe_ins,
            label=translations[lang]["class"], enable_search=True
        )
        self.ins_mat = ft.TextField(
            **underline_field_style, prefix_icon=ft.icons.CREDIT_CARD_OUTLINED, width=250,
            label=translations[lang]["registration number"]
        )
        self.ins_effectif = ft.TextField(
            **underline_field_style, prefix_icon=ft.icons.KEYBOARD_DOUBLE_ARROW_UP_OUTLINED, width=125,
            text_align=ft.TextAlign.RIGHT,
            label=translations[lang]["head count"]
        )
        self.ins_check = ft.Checkbox(
            label=translations[lang]["repeater_ins"], label_style=ft.TextStyle(**text_title_style),
            active_color="#f0f0f6", check_color=SECONDARY_COLOR
        )
        self.ins_frais = ft.TextField(
            **underline_field_style, prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED, width=150,
            text_align=ft.TextAlign.RIGHT,
            label=translations[lang]["fees"]
        )
        self.ins_tranche_1 = ft.TextField(
            **field_style_2, width=150, label=translations[lang]["fees part 1"],
            input_filter=ft.NumbersOnlyInputFilter(),
            prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED,
            text_align=ft.TextAlign.RIGHT
        )
        self.ins_tranche_2 = ft.TextField(
            **field_style_2, width=150, label=translations[lang]["fees part 2"],
            input_filter=ft.NumbersOnlyInputFilter(),
            prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED,
            text_align=ft.TextAlign.RIGHT
        )
        self.ins_tranche_3 = ft.TextField(
            **field_style_2, width=150, label=translations[lang]["fees part 3"],
            input_filter=ft.NumbersOnlyInputFilter(),
            prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED,
            text_align=ft.TextAlign.RIGHT
        )
        self.ins_switch = ft.Switch(
            active_color=ft.colors.GREY, thumb_color=SECONDARY_COLOR, track_outline_color="black",
            scale=0.7, on_change=self.changement_solde_ins,
        )
        self.ins_nom = ft.Text(
            size=24, color=MAIN_COLOR, font_family="PPL"
        )
        self.ins_prenom = ft.Text(
            size=14, color="white", font_family="PPL", visible=False
        )
        self.ins_id= ft.Text(
            size=14, color="white", font_family="PPL", visible=False
        )
        self.inscription_frame = ft.Card(
            elevation=50, surface_tint_color="white", width=700, height=575, expand=True,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                padding=10, bgcolor="white",
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Container(
                            padding=10, bgcolor="#f0f0f6", border_radius=12,
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.PERSON_ADD_OUTLINED, size=20, color="black"),
                                            ft.Text(translations[lang]["register form"].upper(), size=16,
                                                    font_family="PPB", ),
                                        ]
                                    ),
                                    ft.IconButton(
                                        'close', scale=0.7, icon_color=MAIN_COLOR, bgcolor="#f0f0f6",
                                        on_click=self.close_inscription_frame,
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=10, bgcolor="white", border_radius=12, expand=True,
                            content=ft.Column(
                                expand=True, scroll=ft.ScrollMode.AUTO,
                                controls=[
                                    ft.Container(
                                        padding=ft.padding.only(10, 0, 10, 0), content=ft.Column(
                                            controls=[
                                                ft.Column(
                                                    controls=[
                                                        self.ins_nom, self.ins_prenom, self.ins_id,
                                                        ft.Divider(height=1, color=MAIN_COLOR)
                                                    ], spacing=0
                                                ),
                                                ft.Divider(height=1, color=ft.Colors.TRANSPARENT),
                                                ft.Row(
                                                    controls=[
                                                        ft.Text(translations[lang]["academic year"].upper(), size=12,
                                                                font_family="PPM"),
                                                        ft.TextField(
                                                            **underline_field_style,
                                                            prefix_icon=ft.icons.EDIT_CALENDAR_OUTLINED,
                                                            width=90, value=running_year()
                                                        ),
                                                        ft.Row([self.ins_class, self.ins_effectif]),
                                                    ]
                                                ),
                                                ft.Row([self.ins_mat, self.ins_frais]),
                                                self.ins_check,
                                                ft.Divider(height=1, color=ft.colors.TRANSPARENT),
                                                ft.Column(
                                                    controls=[
                                                        ft.Text(translations[lang]["school fees"].upper(), size=12,
                                                                font_family="PPB", color=MAIN_COLOR),
                                                        ft.Divider(height=1, thickness=1),
                                                    ], spacing=0
                                                ),
                                                ft.Row(
                                                    [
                                                        ft.Text(translations[lang]['pay off'].upper(), size=12,
                                                                font_family="PPM"),
                                                        self.ins_switch
                                                    ]
                                                ),
                                                ft.Row(
                                                    controls=[
                                                        self.ins_tranche_1, self.ins_tranche_2, self.ins_tranche_3
                                                    ]
                                                ),
                                                ElevBt(translations[lang]['valid'], MAIN_COLOR, 150, self.inscrire_ancien_eleve)
                                            ], spacing=15
                                        )
                                    )
                                ], spacing=5
                            )
                        )
                    ], spacing=20
                )
            )
        )

        # Paiements ...
        self.pay_name = ft.Text(size=24, font_family="PPL", color='black')
        self.pay_id = ft.Text(visible=False)
        self.pay_fees = ft.Text(size=24, font_family="PPL")
        self.pay_pb_pension = ft.ProgressBar(
            height=8, width=120, border_radius=10, bgcolor="grey",
        )
        self.table_tranches = ft.DataTable(
            data_text_style=ft.TextStyle(size=12, font_family="PPM", color="black"),
            heading_text_style=ft.TextStyle(size=12, font_family="PPM", color="grey"),
            columns=[
                ft.DataColumn(ft.Text("asco")), ft.DataColumn(ft.Text("date")),
                ft.DataColumn(ft.Text("tranche")), ft.DataColumn(ft.Text("montant"))
            ]
        )

        self.pay_switch_t1 = ft.Switch(
            active_color=ft.colors.GREY, thumb_color=SECONDARY_COLOR, track_outline_color="black",
            scale=0.7, on_change=self.changement_solde_ins,
        )
        self.pay_switch_t2 = ft.Switch(
            active_color=ft.colors.GREY, thumb_color=SECONDARY_COLOR, track_outline_color="black",
            scale=0.7, on_change=self.changement_solde_ins,
        )
        self.pay_switch_t3 = ft.Switch(
            active_color=ft.colors.GREY, thumb_color=SECONDARY_COLOR, track_outline_color="black",
            scale=0.7, on_change=self.changement_solde_ins,
        )
        self.pay_t1 = ft.TextField(
            **field_style_2, border=ft.InputBorder.UNDERLINE, width=120,
            input_filter=ft.NumbersOnlyInputFilter(),
            prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED,
            text_align=ft.TextAlign.RIGHT
        )
        self.pay_box_t1 = ft.Container(
            padding=20, border=ft.border.all(1, "grey"), border_radius=12,
            content = ft.Column(
                controls=[
                    ft.Text(f"{translations[lang]['fees part 1']}".upper(), size=13, font_family="PPB"),
                    ft.Text("Montant tranche 1: 75 000", size=11, color="grey", font_family="PPI"),
                    self.pay_t1
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        self.pay_t2 = ft.TextField(
            **field_style_2, border=ft.InputBorder.UNDERLINE, width=120,
            input_filter=ft.NumbersOnlyInputFilter(),
            prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED,
            text_align=ft.TextAlign.RIGHT
        )
        self.pay_box_t2 = ft.Container(
            padding=20, border=ft.border.all(1, "grey"), border_radius=12,
            content=ft.Column(
                controls=[
                    ft.Text(f"{translations[lang]['fees part 2']}".upper(), size=13, font_family="PPB"),
                    ft.Text("Montant tranche 2: 30 000", size=11, color="grey", font_family="PPI"),
                    self.pay_t2
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        self.pay_t3 = ft.TextField(
            **field_style_2, border=ft.InputBorder.UNDERLINE, width=120,
            input_filter=ft.NumbersOnlyInputFilter(),
            prefix_icon=ft.icons.MONETIZATION_ON_OUTLINED,
            text_align=ft.TextAlign.RIGHT
        )
        self.pay_box_t3 = ft.Container(
            padding=20, border=ft.border.all(1, "grey"), border_radius=12,
            content=ft.Column(
                controls=[
                    ft.Text(f"{translations[lang]['fees part 3']}".upper(), size=13, font_family="PPB"),
                    ft.Text("Montant tranche 3: 15 000", size=11, color="grey", font_family="PPI"),
                    self.pay_t3
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        self.paiements_frame = ft.Card(
            elevation=50, surface_tint_color="white", width=700, height=575, expand=True,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, scale=ft.transform.Scale(0),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            content=ft.Container(
                padding=10, bgcolor="white",
                content=ft.Column(
                    expand=True,
                    controls=[
                        ft.Container(
                            padding=10, bgcolor="#f0f0f6", border_radius=12,
                            content=ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Icon(ft.icons.ADD_CARD_OUTLINED, size=20, color="black"),
                                            ft.Text(translations[lang]["fees form"].upper(), size=16,
                                                    font_family="PPB", ),
                                        ]
                                    ),
                                    ft.IconButton(
                                        'close', scale=0.7, icon_color=MAIN_COLOR, bgcolor="#f0f0f6",
                                        on_click=None
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ),
                        ft.Container(
                            padding=10, bgcolor="white", border_radius=12, expand=True,
                            content=ft.Column(
                                expand=True,
                                controls=[
                                    ft.Row(
                                        controls=[
                                            self.pay_name,
                                            ft.Row(
                                                [self.pay_pb_pension,  self.pay_fees, self.pay_id,]
                                            ),
                                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    ),
                                    ft.Divider(height=2, thickness=1),
                                    ft.Divider(height=2, color=ft.Colors.TRANSPARENT),

                                    ft.ListView([self.table_tranches], expand=True, height=100),
                                    ft.Divider(height=2, color=ft.Colors.TRANSPARENT),
                                    ft.Row(
                                        controls=[
                                            self.pay_box_t1, self.pay_box_t2, self.pay_box_t3
                                        ]
                                    )
                                ]
                            )
                        )
                    ], spacing=20
                )
            )
        )

        self.main_window = ft.Container(
            bgcolor="white", padding=10, border_radius=12, expand=True,
            content=ft.Stack(
                expand=True,
                controls=[
                    ft.Column(
                        expand=True,
                        controls=[
                            ft.Container(
                                bgcolor="white", padding=ft.padding.only(20, 20, 20, 20),
                                border_radius=12,
                                content=ft.Row(
                                    controls=[
                                        ft.Row(
                                            controls=[
                                                self.filtre_eleves,
                                                ft.Row([self.bt_filtres, self.bt_supp_filtres], spacing=5)
                                            ], spacing=10
                                        ),
                                        self.results,

                                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                            ),
                            ft.Divider(height=1, color=ft.Colors.TRANSPARENT),
                            ft.Text("Liste des élèves", size=14, font_family="PPB"),
                            self.list,
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    self.bt_new_elev
                ], alignment=ft.alignment.bottom_right
            )
        )

        self.content = ft.Stack(
            expand=True,
            controls=[
               self.main_window, self.new_elv_frame, self.edit_elv_frame,
                self.inscription_frame, self.paiements_frame
            ], alignment=ft.alignment.center
        )
        self.load_datas()
        self.load_lists()

    def load_lists(self):
        classes = all_classes()
        for classe in classes:
            self.n_class.options.append(
                ft.dropdown.Option(classe['code'])
            )
            self.ins_class.options.append(
                ft.dropdown.Option(classe['code'])
            )

    def load_datas(self):
        eleves = all_eleves()

        self.results.value = f"{len(eleves)} Résultats"

        for widget in self.list.controls[:]:
            self.list.controls.remove(widget)

        for data in eleves:
            self.list.controls.append(FicheEleve(self, data))

    def filter_datas(self, e):
        liste_eleves = all_eleves()

        search = self.filtre_eleves.value.lower() if self.filtre_eleves.value.lower() is not None else ""

        filtered_liste = list(filter(lambda row: search in row['nom'].lower(), liste_eleves))

        for widget in self.list.controls[:]:
            self.list.controls.remove(widget)

        self.results.value = f"{len(filtered_liste)} Résultats" if len(filtered_liste) >= 2 else f"{len(filtered_liste)} Résultat"
        self.results.update()

        for data in filtered_liste:
            self.list.controls.append(FicheEleve(self, data))

        self.list.update()

    def supp_filter(self, e):
        self.filtre_eleves.value = None
        self.filtre_eleves.update()
        self.load_datas()
        self.list.update()
        self.results.update()

    def changement_solde_new(self, e):
        if self.n_switch.value:
            self.n_tranche_3.value = montant_tranche('tranche 3')
            self.n_tranche_2.value = montant_tranche('tranche 2')
            self.n_tranche_1.value = montant_tranche('tranche 1')
            self.n_tranche_3.update()
            self.n_tranche_2.update()
            self.n_tranche_1.update()

        else:
            self.n_tranche_3.value = None
            self.n_tranche_2.value = None
            self.n_tranche_1.value = None
            self.n_tranche_3.update()
            self.n_tranche_2.update()
            self.n_tranche_1.update()

    def changement_classe_new(self, e):
        self.n_effectif.value = str(nb_inscrits_classe(self.n_class.value))
        self.n_effectif.update()
        self.n_frais.value = str(montant_tranche('inscription'))
        self.n_frais.update()

        mat = create_new_matricule()

        self.n_mat.value = mat
        self.n_mat.update()

    def change_date_new_elev(self, e):
        self.n_sel_date.value = str(self.cp.dp_new_eleve.value)[0:10]
        self.n_sel_date.update()

    def close_new_elv_frame(self, e):
        self.new_elv_frame.scale = 0
        self.new_elv_frame.update()

    def open_new_elv_frame(self, e):
        self.new_elv_frame.scale = 1
        self.new_elv_frame.update()

    def select_image(self, e: ft.FilePickerResultEvent):
        if not e.files:
            pass
        else:
            file = e.files[0]
            file_path = file.path
            file_name = os.path.basename(file_path)

            # Détecter le type MIME du fichier
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = "application/octet-stream"  # Valeur par défaut si type non trouvé

            # Si c'est une image .jpg ou .jpeg, on assure que le type MIME est bien 'image/jpeg'
            if file_name.lower().endswith(('.jpg', '.jpeg')):
                mime_type = 'image/jpeg'

            try:
                with open(file_path, "rb") as f:
                    file_data = f.read()

                    # Téléchargement vers Supabase sans spécifier le type MIME pour l'instant
                    response = supabase.storage.from_(BUCKET_NAME).upload(file_name, file_data)

                    if response:
                        # URL publique de l'image téléchargée
                        url = supabase.storage.from_(BUCKET_NAME).get_public_url(file_name)

                        # Mise à jour de l'interface avec l'image téléchargée
                        self.new_image_box.content.src = url
                        self.new_image_box.content.fit = ft.ImageFit.CONTAIN
                        self.new_image_box.update()
                    else:
                        self.cp.box.title.value = "Erreur"
                        self.cp.box.content.value = "Upload impossible"
                        self.cp.box.open = True
                        self.cp.box.update()

            except Exception as ex:
                self.cp.box.title.value = "Erreur"
                self.cp.box.content.value = f"Erreur {ex}"
                self.cp.box.open = True
                self.cp.box.update()

    def create_eleve(self, e):
        count = 0
        for widget in (self.n_name, self.n_contact, self.n_class, self.sexe, self.n_surname):
            if widget.value is None or widget.value == "":
                count += 1

        if count > 0:
            self.cp.box.title.value = f"{translations[lang]['error title']}"
            self.cp.box.content.value = f"{translations[lang]['error msg']}"
            self.cp.box.open = True
            self.cp.box.update()
        else:
            add_eleve(
                self.n_name.value, self.n_surname.value, self.sexe.value, self.n_sel_date.value, self.n_lieu.value,
                self.n_pere.value, self.n_mere.value, self.n_contact.value, self.n_autre.value, self.n_mat.value,
                self.new_image_box.url
            )

            eleves = all_eleves()
            length = len(eleves)
            last_id = eleves[length - 1]['id']

            asco = running_year()

            for tranche in (self.n_tranche_1, self.n_tranche_2, self.n_tranche_3):
                if tranche.value is None or tranche.value == "":
                    pass
                else:
                    mt = int(tranche.value)
                    if tranche.label == "Tranche 1" or tranche.label == "fees part 1":
                        name_tranche = 'tranche 1'
                    elif tranche.label == "Tranche 2" or tranche.label == "fees part 2":
                        name_tranche = 'tranche 2'
                    else:
                        name_tranche = 'tranche 3'

                    add_pension(last_id, name_tranche, mt)

            for tranche in (self.n_tranche_1, self.n_tranche_2, self.n_tranche_3):
                tranche.value = None
                tranche.update()

            self.n_switch.value = False
            self.n_switch.update()

            statut = "nouveau".upper() if self.n_check.value is False else "redoublant".upper()

            # Ajouter inscription
            add_inscription(last_id, self.n_mat.value, self.n_class.value, self.n_frais.value, statut)

            for widget in (
                self.n_name, self.n_contact, self.n_class, self.sexe, self.n_lieu, self.n_mat, self.n_pere,
                self.n_mere, self.n_sel_date, self.n_contact, self.n_class, self.n_frais, self.n_surname, self.n_autre,
                self.n_effectif, self.n_check
            ):
                widget.value = None
                widget.update()

            self.cp.box.title.value = f"{translations[lang]['confirm title']}"
            self.cp.box.content.value = f"{translations[lang]['confirm msg']}"
            self.cp.box.open = True
            self.cp.box.update()

            self.load_datas()
            self.list.update()
            self.results.update()

    def close_edit_elv_frame(self, e):
        self.edit_elv_frame.scale = 0
        self.edit_elv_frame.update()

    def change_date_edit_elev(self, e):
        self.sel_date.value = str(self.cp.dp_modif_eleve.value)[0:10]
        self.sel_date.update()

    def changer_sexe(self, e):
        if self.edit_sexe.value == "MASCULIN":
            self.edit_sexe.value = "FEMININ"
        else:
            self.edit_sexe.value = "MASCULIN"

        self.edit_sexe.update()

    def select_edit_image(self, e: ft.FilePickerResultEvent):
        if not e.files:
            pass
        else:
            file = e.files[0]
            file_path = file.path
            file_name = os.path.basename(file_path)

            # Détecter le type MIME du fichier
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = "application/octet-stream"  # Valeur par défaut si type non trouvé

            # Si c'est une image .jpg ou .jpeg, on assure que le type MIME est bien 'image/jpeg'
            if file_name.lower().endswith(('.jpg', '.jpeg')):
                mime_type = 'image/jpeg'

            try:
                with open(file_path, "rb") as f:
                    file_data = f.read()

                    # Téléchargement vers Supabase sans spécifier le type MIME pour l'instant
                    response = supabase.storage.from_(BUCKET_NAME).upload(file_name, file_data)

                    if response:
                        # URL publique de l'image téléchargée
                        url = supabase.storage.from_(BUCKET_NAME).get_public_url(file_name)

                        # Mise à jour de l'interface avec l'image téléchargée
                        self.edit_image_box.content.src = url
                        self.edit_image_box.content.fit = ft.ImageFit.CONTAIN
                        self.edit_image_box.update()
                    else:
                        self.cp.box.title.value = "Erreur"
                        self.cp.box.content.value = "Upload impossible"
                        self.cp.box.open = True
                        self.cp.box.update()

            except Exception as ex:
                self.cp.box.title.value = "Erreur"
                self.cp.box.content.value = f"Erreur {ex}"
                self.cp.box.open = True
                self.cp.box.update()

    def modifier_eleve(self, e):
        count = 0
        for widget in (self.edit_nom, self.edit_tel, self.edit_sexe, self.edit_pere, self.edit_mere, self.sel_date, self.edit_lieu, self.edit_prenom):
            if widget.value is None or widget.value == "":
                count += 1

        if count > 0:
            self.cp.box.title.value = f"{translations[lang]['error title']}"
            self.cp.box.content.value = f"{translations[lang]['error msg']}"
            self.cp.box.open = True
            self.cp.box.update()
        else:
            update_eleve(
                self.edit_nom.value, self.edit_prenom.value, self.edit_sexe.value, self.sel_date.value, self.edit_lieu.value,
                self.edit_pere.value, self.edit_mere.value, self.edit_tel.value, self.edit_autre.value, self.edit_image_box.content.src,
                int(self.edit_id.value)
            )
            self.cp.box.title.value = f"{translations[lang]['confirm title']}"
            self.cp.box.content.value = f"{translations[lang]['confirm msg']}"
            self.cp.box.open = True
            self.cp.box.update()

            self.edit_elv_frame.scale = 0
            self.edit_elv_frame.update()

            self.load_datas()
            self.list.update()
            self.results.update()

    def changement_solde_ins(self, e):
        if self.ins_switch.value:
            self.ins_tranche_3.value = montant_tranche('tranche 3')
            self.ins_tranche_2.value = montant_tranche('tranche 2')
            self.ins_tranche_1.value = montant_tranche('tranche 1')
            self.ins_tranche_3.update()
            self.ins_tranche_2.update()
            self.ins_tranche_1.update()

        else:
            self.ins_tranche_3.value = None
            self.ins_tranche_2.value = None
            self.ins_tranche_1.value = None
            self.ins_tranche_3.update()
            self.ins_tranche_2.update()
            self.ins_tranche_1.update()

    def close_inscription_frame(self, e):
        self.inscription_frame.scale = 0
        self.inscription_frame.update()

    def changement_classe_ins(self, e):
        self.ins_effectif.value = str(nb_inscrits_classe(self.ins_class.value))
        self.ins_effectif.update()
        self.ins_frais.value = str(montant_tranche('inscription'))
        self.ins_frais.update()

    def inscrire_ancien_eleve(self, e):

        my_classe = self.ins_class.value

        if my_classe == "" or my_classe is None:
            pass

        else:
            id_eleve = int(self.ins_id.value)
            asco = running_year()

            for tranche in (self.ins_tranche_1, self.ins_tranche_2, self.ins_tranche_3):
                if tranche.value is None or tranche.value == "":
                    pass
                else:
                    mt = int(tranche.value)
                    if tranche.label == "Tranche 1" or tranche.label == "fees part 1":
                        name_tranche = 'tranche 1'
                    elif tranche.label == "Tranche 2" or tranche.label == "fees part 2":
                        name_tranche = 'tranche 2'
                    else:
                        name_tranche = 'tranche 3'

                    add_pension(id_eleve, name_tranche, mt)

            for tranche in (self.ins_tranche_1, self.ins_tranche_2, self.ins_tranche_3):
                tranche.value = None
                tranche.update()

            self.ins_switch.value = False
            self.ins_switch.update()

            statut = "nouveau".upper() if self.ins_check.value is False else "redoublant".upper()

            # Ajouter inscription
            add_inscription(id_eleve, self.ins_mat.value, self.ins_class.value, self.ins_frais.value, statut)

            for widget in (
                self.ins_class, self.ins_mat, self.ins_frais,
                self.ins_effectif, self.ins_check
            ):
                widget.value = None
                widget.update()

            self.cp.box.title.value = f"{translations[lang]['confirm title']}"
            self.cp.box.content.value = f"{translations[lang]['confirm msg']}"
            self.cp.box.open = True
            self.cp.box.update()

            self.load_datas()
            self.list.update()
            self.results.update()

