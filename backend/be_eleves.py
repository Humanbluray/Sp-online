from supabase import create_client
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2 import pool
import datetime

# Chargement des varaiables d'environnement
load_dotenv()

# Configuration du client supabase
URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")
supabase = create_client(URL, KEY)

SUPA_DATABASE = os.getenv('SUPA_DATABASE')
SUPA_USER = os.getenv('SUPA_USER')
SUPA_PASSWORD = os.getenv('SUPA_PASSWORD')
SUPA_PORT = os.getenv('SUPA_PORT')
SUPA_HOST = os.getenv('SUPA_HOST')

# # Créer un pool de connexions
# connection_pool = psycopg2.pool.SimpleConnectionPool(
#     1, 10,  # Min et max de connexions
#     host=SUPA_HOST, user=SUPA_USER, password=SUPA_PASSWORD, database=SUPA_DATABASE, port=SUPA_PORT
# )
#
# def get_db_connection():
#     return connection_pool.getconn()
#
#
# def release_db_connection(conn):
#     connection_pool.putconn(conn)


def all_eleves():
    resp = supabase.table("eleves").select("*").execute()
    return resp.data


def running_year():
    resp = supabase.table("annees").select("*").eq("statut", "en cours").execute()
    return resp.data[0]['nom']


def all_classes():
    resp = supabase.table("classes").select("*").execute()
    return resp.data


def total_pension():
    resp = supabase.table("tranches").select("*").eq("pension", True).eq("asco", running_year()).execute()
    total = 0
    for row in resp.data:
        total += row["montant"]
    return total


def montant_tranche(tranche):
    resp = supabase.table("tranches").select("montant").eq("nom", tranche).eq("asco", running_year()).execute()
    return resp.data[0]['montant']


def nb_inscrits_classe(classe):
    resp = supabase.table("inscriptions").select("*").eq("classe", classe).eq("asco", running_year()).execute()
    return len(resp.data)


def nb_inscrits():
    resp = supabase.table("inscriptions").select("*").eq("asco", running_year()).execute()
    return len(resp.data)


def create_new_matricule():
    nb_registrations = nb_inscrits() + 1

    if 1 <= nb_registrations < 10:
        zero = "00"
    elif 10 <= nb_registrations < 100:
        zero = "0"
    else:
        zero = ""

    mat = "CBK" + str(running_year()) + zero + str(nb_registrations)

    return mat


def add_eleve(nom, prenom, sexe, naissance, lieu, pere, mere, contact, autre, matricule, image):
    supabase.table("eleves").insert(
        {
            'nom': nom,  'prenom': prenom, 'sexe': sexe, 'naissance': naissance, 'lieu': lieu, 'pere': pere,
            'mere': mere, 'contact': contact, 'autre': autre, 'matricule': matricule, 'image': image
        }
    ).execute()


def add_pension(id_eleve, tranche, montant):
    supabase.table("pensions").insert(
        {"asco": running_year(), "id_eleve": id_eleve, "tranche": tranche, "montant": montant}
    ).execute()


def pension_by_eleve(id_eleve: int):
    resp = supabase.table("pensions").select("*").eq("id_eleve", id_eleve).eq("asco", running_year()).execute()
    total = 0

    if not resp.data:
        total = 0
    else:
        for row in resp.data:
            total += row['montant']

    return total


def detail_pension_by_eleve(id_eleve: int):
    resp = supabase.table("pensions").select("*").eq("id_eleve", id_eleve).eq("asco", running_year()).execute()
    return resp.data


def add_inscription(id_elev, matricule, classe, frais, statut):
    supabase.table("inscriptions").insert(
        {"asco": running_year(), "id_eleve": id_elev, "matricule": matricule, "classe": classe, "frais": frais, "statut": statut}
    ).execute()


def update_eleve(nom, prenom, sexe, date, lieu, pere, mere,contact, autre, image, id_eleve):
    supabase.table("eleves").update(
        {"nom": nom, "prenom": prenom, "sexe": sexe, "naissance": date, "lieu": lieu, "pere": pere,
         "mere": mere, "contact": contact, "autre": autre, "image": image}
    ).eq("id", id_eleve).execute()


def is_inscrit(id_eleve):
    resp = supabase.table("inscriptions").select("*").eq("id_eleve", id_eleve).eq("asco", running_year()).execute()
    return True if resp.data else False



# print(nb_inscrits_classe('Tle D I'))