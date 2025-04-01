import flet as ft
from utils import MAIN_COLOR, SECONDARY_COLOR
from backend.be_eleves import *
from utils.useful_functions import ajout_separateur_virgule
import asyncio


class FicheEleve(ft.Container):
    def __init__(self, cp: object, data: dict):
        super().__init__(padding=ft.padding.only(20, 10, 20, 10), bgcolor="white", border_radius=16)
        self.cp = cp
        self.data = data

        if is_inscrit(self.data['id']):
            color = ft.Colors.GREEN
            bgcolor = ft.Colors.GREEN_50
            texte = "inscrit"
            icone = ft.icons.CHECK_CIRCLE
            disabled_inscrire = True
            disabled_paiements = False

        else:
            color = ft.Colors.GREY
            bgcolor = ft.Colors.GREY_50
            texte = 'Non inscrit'
            icone = ft.icons.STOP
            disabled_inscrire = False
            disabled_paiements = True

        # all_pensions = []
        # for data in pensions:
        #     dico = {
        #         'asco': data[0], 'eleve': data[1], 'classe': data[2], 'versé': data[5], 'pension': data[4],
        #         'reste': data[6], 'statut': data[7],
        #     }
        #     all_pensions.append(dico)
        #
        # my_pension = 0
        # total = 0
        # for row in all_pensions:
        #     if be.is_inscriptions_exists(self.data['nom'], self.data['matricule']):
        #         if row["eleve"] == self.data['nom']:
        #             my_pension += row['versé']
        #             total += row['pension']
        #     else:
        #         my_pension = 0
        #         total = be.total_pension()
        #
        # percent = my_pension * 100 / total
        #
        # if my_pension == total:
        #     pb_couleur = ft.Colors.LIGHT_GREEN
        #
        # elif 0 < percent < 33:
        #     pb_couleur = ft.Colors.RED
        #
        # elif 33 <= percent < 66:
        #     pb_couleur = ft.Colors.DEEP_ORANGE
        #
        # else:
        #     pb_couleur = ft.Colors.AMBER
        #
        # self.pb_pension = ft.ProgressBar(
        #     value=my_pension/total, bar_height=7, width=100, border_radius=10, bgcolor="grey", color=pb_couleur
        # )
        # optimized_url = f"{self.data['image']}?width=100&height=100&format=webp"
        # place_holder = "https://nppwkqytgqlqijpeulfj.supabase.co/storage/v1/object/public/profs_pictures//homme.webp"
        # self.image_widget = ft.Image(src=place_holder)

        self.content = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Column(
                                        controls=[
                                            ft.Text(f"{self.data['nom'].upper()}", size=13, font_family="PPM"),
                                            ft.Text(
                                                f"{self.data['prenom'].upper()}", size=12, font_family="PPM",
                                                color="grey"
                                            ),
                                        ], spacing=0
                                    ),
                                    ft.Container(
                                        border_radius=10, padding=ft.padding.only(3, 2, 3, 2),
                                        bgcolor=bgcolor, border=ft.border.all(1, color),
                                        content=ft.Row(
                                            controls=[
                                                ft.Icon(icone, color=color, size=11),
                                                ft.Text(texte, size=10, font_family="PPM", color=color),
                                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=0
                                        )
                                    ),
                                ], spacing=10
                            )
                        ),
                    ]
                ),
                ft.PopupMenuButton(
                    # content=ft.Icon(ft.Icons.PENDING_ACTIONS_OUTLINED, size=24, color="black"),
                    bgcolor="white", icon_color="black",
                    items=[
                        ft.PopupMenuItem(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.icons.EDIT_OUTLINED, color=ft.Colors.BLACK54, size=24),
                                    ft.Text("Modifier", size=14, font_family="PPM", color=ft.Colors.BLACK87)
                                ], alignment=ft.MainAxisAlignment.START, spacing=10
                            ), on_click=self.open_dit_window
                        ),
                        ft.PopupMenuItem(
                            disabled=disabled_inscrire,
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.icons.BOOKMARK_OUTLINE_ROUNDED, color=ft.Colors.BLACK54, size=24),
                                    ft.Text("Inscrire", size=14, font_family="PPM", color=ft.Colors.BLACK87)
                                ], alignment=ft.MainAxisAlignment.START, spacing=10,
                            ), on_click=self.open_inscriptions_window
                        ),
                        ft.PopupMenuItem(
                            disabled=disabled_paiements,
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.icons.MONETIZATION_ON_OUTLINED, color=ft.Colors.BLACK54, size=24),
                                    ft.Text("Paiements", size=14, font_family="PPM", color=ft.Colors.BLACK87)
                                ], alignment=ft.MainAxisAlignment.START, spacing=10
                            ), on_click=self.open_paiement_frame
                        ),
                    ],
                )

            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

    def open_dit_window(self, e):
        self.cp.edit_image_box.content.src = self.data['image']
        self.cp.edit_image_box.update()

        self.cp.edit_nom.value = self.data['nom']
        self.cp.edit_nom.update()
        self.cp.edit_prenom.value = self.data['prenom']
        self.cp.edit_prenom.update()

        self.cp.edit_id.value = str(self.data['id'])
        self.cp.edit_id.update()
        self.cp.edit_sexe.value = self.data['sexe']
        self.cp.edit_sexe.update()
        self.cp.edit_pere.value = self.data['pere']
        self.cp.edit_pere.update()
        self.cp.edit_mere.value = self.data['mere']
        self.cp.edit_mere.update()
        self.cp.edit_tel.value = self.data['contact']
        self.cp.edit_tel.update()
        self.cp.edit_lieu.value = self.data['lieu']
        self.cp.edit_lieu.update()
        self.cp.sel_date.value = self.data['naissance']
        self.cp.sel_date.update()
        self.cp.edit_picture = self.data['image']

        self.cp.edit_elv_frame.scale = 1
        self.cp.edit_elv_frame.update()

    def open_inscriptions_window(self, e):
        self.cp.ins_nom.value = f"{self.data['nom']}".capitalize()
        self.cp.ins_prenom.value = f"{self.data['prenom']}".capitalize()
        self.cp.ins_nom.update()
        self.cp.ins_prenom.update()

        self.cp.ins_mat.value = f"{self.data['matricule']}"
        self.cp.ins_mat.update()

        self.cp.ins_id.value = str(self.data['id'])
        self.cp.ins_id.update()

        self.cp.inscription_frame.scale = 1
        self.cp.inscription_frame.update()

    def open_paiement_frame(self, e):
        self.cp.pay_name.value = f"{self.data['nom']}"
        self.cp.pay_name.update()
        self.cp.pay_id.value = f"{self.data['id']}"
        self.cp.pay_id.update()

        my_pension = pension_by_eleve(self.data['id'])
        self.cp.pay_fees.value = f"{ajout_separateur_virgule(my_pension)}"
        self.cp.pay_fees.update()

        annual_fees = montant_tranche('tranche 1') + montant_tranche('tranche 2') + montant_tranche('tranche 3')
        percent = my_pension * 100 / annual_fees

        if my_pension == annual_fees:
            pb_couleur = ft.Colors.LIGHT_GREEN

        elif 0 < percent < 33:
            pb_couleur = ft.Colors.RED

        elif 33 <= percent < 66:
            pb_couleur = ft.Colors.DEEP_ORANGE

        else:
            pb_couleur = ft.Colors.AMBER

        self.cp.pay_pb_pension.value = percent / 100
        self.cp.pay_pb_pension.color = pb_couleur
        self.cp.pay_pb_pension.update()


        for row in self.cp.table_tranches.rows[:]:
            self.cp.table_tranches.rows.remove(row)

        for row in detail_pension_by_eleve(self.data['id']):
            self.cp.table_tranches.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"{row['asco']}")),
                        ft.DataCell(ft.Text(f"{row['date']}")),
                        ft.DataCell(ft.Text(f"{row['tranche']}")),
                        ft.DataCell(ft.Text(f"{row['montant']}")),
                    ]
                )
            )

        self.cp.table_tranches.update()

        self.cp.paiements_frame.scale = 1
        self.cp.paiements_frame.update()

