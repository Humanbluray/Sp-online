import os
import flet as ft
from pages.landing.landing import Connexion
from pages.accueil.accueil import Accueil

ROUTE_CONNEXION = "/"
ROUTE_ACCUEIL = "/accueil"

def main(page: ft.Page):
    # Charger les polices personnalisées
    page.fonts = {
        "PPR": "fonts/Poppins-Regular.ttf",
        "PPB": "fonts/Poppins-Bold.ttf",
        "PPSB": "fonts/Poppins-SemiBold.ttf",
        "PPBL": "fonts/Poppins-Black.ttf",
        "PPI": "fonts/Poppins-Italic.ttf",
        "PPM": "fonts/Poppins-Medium.ttf",
        "PPEB": "fonts/Poppins-ExtraBold.ttf",
        "PPL": "fonts/Poppins-Light.ttf",
        "UBB": "fonts/Urbanist-Bold.ttf",
        "UBI": "fonts/Urbanist-Italic.ttf",
        "UBM": "fonts/Urbanist Medium.ttf",
        "QSM": "fonts/Quicksand-Medium.ttf",
        "QSR": "fonts/Quicksand-Regular.ttf",
        "QSB": "fonts/Quicksand-Bold.ttf",
    }
    page.title = "School Pilot"
    page.theme_mode = ft.ThemeMode.LIGHT

    # Dictionnaire pour mapper les routes aux vues
    route_views = {
        ROUTE_CONNEXION: Connexion,
        ROUTE_ACCUEIL: Accueil,
    }

    # Gérer les changements de route
    def route_change(event: ft.RouteChangeEvent):
        page.views.clear()  # Réinitialiser les vues
        current_route = event.route  # Récupérer la route depuis l'événement
        if current_route in route_views:
            page.views.append(route_views[current_route](page))
        else:
            # Rediriger vers une route par défaut si la route est inconnue
            page.views.append(Connexion(page))
        page.update()

    # Gérer la navigation "retour"
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # Assignation des callbacks
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Naviguer vers la route initiale
    page.go(page.route)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    ft.app(target=main, assets_dir="assets", route_url_strategy="default",)