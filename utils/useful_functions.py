import datetime

# 1. Fonctions générales
def ajout_separateur(nombre):
    nombre = str(nombre)[::-1]
    resultat = ""
    for i, numero in enumerate(nombre, 1):
        numero_formatte = numero + " " if i % 3 == 0 and i != len(nombre) else numero
        resultat += numero_formatte
    return resultat[::-1]


def ajout_separateur_virgule(nombre):
    nombre = str(nombre)[::-1]
    resultat = ""
    for i, numero in enumerate(nombre, 1):
        numero_formatte = numero + " ," if i % 3 == 0 and i != len(nombre) else numero
        resultat += numero_formatte
    return resultat[::-1]


def convert_date(day):
    jr = int(day[0: 2])
    mt = int(day[3: 5])
    an = int(day[6:])
    resultat = datetime.date(an, mt, jr)
    return resultat


def ecrire_nombre(that_number: float):
    return int(that_number) if that_number == int(that_number) else f"{that_number:.2f}"

