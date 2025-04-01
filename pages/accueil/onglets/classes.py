import json
from utils import *
from utils.styles import *


class Affectation(ft.Container):
    def __init__(self, cp: object, prof: str, classe: str, matiere: str, nb_heures: int, jour: str, creneau: str):
        super().__init__()