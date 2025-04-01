import pandas as pd
import json

# Charger le fichier Excel
# df = pd.read_excel("config.xlsx")  # Remplace par le nom de ton fichier
#
# # Convertir les données en dictionnaire
# translations = {
#     "fr": dict(zip(df["clé"], df["français"])),
#     "en": dict(zip(df["clé"], df["anglais"]))
# }
#
# # Sauvegarder en JSON
# with open("translations.json", "w", encoding="utf-8") as f:
#     json.dump(translations, f, indent=4, ensure_ascii=False)
#
# print("Traductions enregistrées dans translations.json")



# Charger les traductions
with open("translations.json", "r", encoding="utf-8") as f:
    translations = json.load(f)

lang = "en"  # Exemple : récupérer la langue depuis la config
