import sqlite3
import datetime
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import pool

load_dotenv()
SUPA_DATABASE = os.getenv('SUPA_DATABASE')
SUPA_USER = os.getenv('SUPA_USER')
SUPA_PASSWORD = os.getenv('SUPA_PASSWORD')
SUPA_PORT = os.getenv('SUPA_PORT')
SUPA_HOST = os.getenv('SUPA_HOST')

my_base = "Ecole.db"

def convert_binary(filename):
    with open(filename, 'rb') as file:
        photo_image = file.read()
        return photo_image


def trouver_cote(note):
    if float(note) < 10:
        apprec = "D"
    elif 10 <= float(note) < 12:
        apprec = 'C'

    elif 12 <= float(note) < 14:
        apprec = 'C+'

    elif 14 <= float(note) < 15:
        apprec = 'B'

    elif 15 <= float(note) < 16:
        apprec = 'B+'

    elif 16 <= float(note) < 18:
        apprec = "A"

    else:
        apprec = 'A+'

    return apprec



""" 2. Fonctions de la table années scolaires ________________________________________"""
def find_last_date():
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("SELECT fin FROM annee_scolaire WHERE ann_statut = ?", ("en cours",))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res[0]


def show_asco_encours():
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    statut = ("en cours",)
    c.execute("SELECT nom FROM Annee_scolaire WHERE ann_statut = ?", statut)
    resultat = list(c.fetchone())
    res = resultat[0]
    conn.commit()
    conn.close()
    return res


def add_asco(nom, nom_long, debut, fin, statut):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""INSERT INTO annee_scolaire values (?,?,?,?,?,?)""",
                (cur.lastrowid, nom, nom_long, debut, fin, statut))
    con.commit()
    con.close()


def update_statut_asco(statut, nom):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""UPDATE annee_scolaire SET
                    ann_statut=? 
                    WHERE nom=?""", (statut, nom))
    con.commit()
    con.close()


def all_asco():
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT * FROM annee_scolaire""")
    res = cur.fetchall()
    con.commit()
    con.close()
    return res


def max_asco():
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT fin FROM annee_scolaire ORDER by fin DESC""")
    res = cur.fetchone()
    con.commit()
    con.close()
    return res[0]


def id_asco():
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT id FROM annee_scolaire ORDER by id""")
    res = cur.fetchall()
    r_final = []
    for r in res:
        r_final.append(r[0])
    con.commit()
    con.close()
    return r_final


def search_id_note(nom, asco, sequence, classe, matiere, coeff, note):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT id FROM Notes WHERE 
                    nom=? AND asco = ? AND sequence = ? AND classe = ? AND matiere = ?
                    AND coeff = ? AND note = ?""", (nom, asco, sequence, classe, matiere, coeff, note))
    res = cur.fetchone()
    con.commit()
    con.close()
    return res[0] if res is not None else "introuvable"


def search_id_note_import(nom, asco, sequence, classe, matiere, coeff):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT id FROM Notes WHERE 
                    nom=? AND asco = ? AND sequence = ? AND classe = ? AND matiere = ?
                    AND coeff = ?""", (nom, asco, sequence, classe, matiere, coeff))
    res = cur.fetchone()
    con.commit()
    con.close()
    return res[0] if res is not None else "introuvable"


def search_asco_id(id_ascol):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT * FROM annee_scolaire WHERE id =?""", (id_ascol,))
    res = cur.fetchone()
    con.commit()
    con.close()
    return res


def update_asco2(nom, nomlong, debut, fin, statut, id_ascol):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""UPDATE annee_scolaire SET
                        nom =?,
                        nom_long =?,
                        debut =?,
                        fin =?,
                        ann_statut =?
                        WHERE id =?""", (nom, nomlong, debut, fin, statut, id_ascol))
    con.commit()
    con.close()


def show_asco_encours_tuple():
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    statut = ("en cours",)
    c.execute("SELECT nom FROM annee_scolaire WHERE ann_statut = ?", statut)
    resultat = c.fetchone()
    conn.commit()
    conn.close()
    return resultat


def annee_en_cours():
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    statut = ("en cours",)
    c.execute("SELECT nom FROM annee_scolaire WHERE ann_statut = ?", statut)
    resultat = c.fetchone()
    res = resultat[0]
    conn.commit()
    conn.close()
    return res


""" Fin des Fonctions de la table années scolaires ________________________________________"""

""" 3- Fonctions de la table inscriptions ________________________________"""


def show_all_inscriptions():
    conn = sqlite3.connect(my_base)
    asco = show_asco_encours()
    c = conn.cursor()
    c.execute("SELECT * FROM inscriptions WHERE ins_asco = ?", (asco,))
    resultat = c.fetchall()
    conn.commit()
    conn.close()
    return resultat


def compter_inscrits():
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    asco = show_asco_encours_tuple()
    c.execute("SELECT COUNT(ins_num) from inscriptions WHERE ins_asco = ?", asco)
    resultat = c.fetchone()
    conn.commit()
    conn.close()
    return resultat[0]


def delete_insc(num):
    to_del = convert_tuple(num)
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    c.execute("DELETE from inscriptions WHERE ins_num = ?", to_del)
    conn.commit()
    conn.close()


def search_insc(classe):
    asco = show_asco_encours()
    z = convert_to_like(classe)
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    c.execute("""SELECT * FROM inscriptions WHERE  
                ins_classe = ? 
                AND ins_asco = ?
                ORDER BY ins_num""", (classe, asco))
    result = c.fetchall()
    conn.commit()
    conn.close()
    return result


def elv_ins_fn_classe(matiere, sequence, classe, classe2):
    asco = show_asco_encours()
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT ins_eleve FROM inscriptions LEFT JOIN 

                    (SELECT nom FROM Notes WHERE Notes.matiere =? and Notes.sequence = ? and Notes.classe = ? and Notes.asco = ?) as deja

                    ON inscriptions.ins_eleve = deja.nom 

                    WHERE deja.nom IS NULL and inscriptions.ins_classe = ? and inscriptions.ins_asco = ?""",
                (matiere, sequence, classe, asco, classe2, asco))

    res = cur.fetchall()

    r_final = []

    for r in res:
        r_final.append(r[0])

    con.commit()
    con.close()
    return r_final


def add_inscription(asco, nom, matricule, classe, frais, statut):
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    param = (c.lastrowid, asco, nom, matricule, classe, frais, statut)

    c.execute("INSERT INTO inscriptions values (?,?,?,?,?,?,?)", param)

    conn.commit()
    conn.close()


def nb_inscrits_classe(classe):
    ascol = show_asco_encours()
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    c.execute(
        "SELECT ins_classe, COUNT(ins_num) FROM inscriptions WHERE ins_asco = ? AND ins_classe = ? GROUP BY ins_classe",
        (ascol, classe))
    resultat = c.fetchone()

    conn.commit()
    conn.close()
    return 0 if resultat is None else resultat[1]


def nb_filles_ins(elv, classe):
    e = convert_to_like(elv)
    c = convert_to_like(classe)
    param = (e, c)
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT sex, count(sex) FROM 
                    (SELECT ins_eleve, ins_classe,
                    (SELECT sexe FROM eleves WHERE eleves.nom = inscriptions.ins_eleve ) as sex
                     FROM inscriptions) WHERE sex='F' AND ins_eleve LIKE ? AND ins_classe LIKE ?
                     group by sex""", param)
    res = cur.fetchone()
    con.commit()
    con.close()
    return res[1]


def nb_garcons_ins(elv, classe):
    e = convert_to_like(elv)
    c = convert_to_like(classe)
    param = (e, c)
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT sex, count(sex) FROM 
                    (SELECT ins_eleve, ins_classe,
                    (SELECT sexe FROM eleves WHERE eleves.nom = inscriptions.ins_eleve ) as sex
                     FROM inscriptions) WHERE sex='M' AND ins_eleve LIKE ? AND ins_classe LIKE ?
                     group by sex""", param)
    res = cur.fetchone()
    con.commit()
    con.close()
    return res[1]


def show_det_insc(classe):
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    asco = show_asco_encours()
    c.execute("SELECT * FROM inscriptions WHERE ins_classe = ? AND ins_asco =? ORDER BY ins_eleve", (classe, asco))
    resultat = c.fetchall()
    conn.commit()
    conn.close()
    return resultat


def show_elv_noninscrits():
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    asco = show_asco_encours_tuple()
    cur.execute("""SELECT nom FROM eleves 
                LEFT JOIN (SELECT ins_eleve FROM inscriptions WHERE ins_asco = ?) AS inscrits 
                ON eleves.nom = inscrits.ins_eleve WHERE inscrits.ins_eleve IS NULL ORDER BY eleves.nom""", asco)
    res = cur.fetchall()
    liste = []
    for result in res:
        liste.append(result[0])
    conn.commit()
    conn.close()
    return liste


def eleves_inscrits():
    asco = show_asco_encours()
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT ins_eleve FROM inscriptions WHERE ins_asco = ? ORDER BY ins_eleve""", (asco,))
    liste = []
    resultat = cur.fetchall()
    for res in resultat:
        liste.append(res[0])
    conn.commit()
    conn.close()
    return liste


def nb_inscrits():
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT count(ins_num) FROM inscriptions WHERE ins_asco =?""", (show_asco_encours(),))
    res = cur.fetchone()
    con.commit()
    con.close()
    return res[0]


def nb_inscrits_sexe(sexe):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT count(ins_eleve) FROM
                    (SELECT ins_eleve, 
                    (SELECT sexe FROM eleves WHERE eleves.nom = inscriptions.ins_eleve) as sexe FROM inscriptions WHERE ins_asco = ?)
                    WHERE sexe = ? GROUP BY sexe""", (show_asco_encours(), sexe))
    res = cur.fetchone()
    con.commit()
    con.close()
    return res[0] if res is not None else 0


def nb_ins_classe(classe):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT count(ins_num) FROM inscriptions WHERE ins_asco=? and ins_classe=? GROUP BY ins_classe""",
                (show_asco_encours(), classe,))
    res = cur.fetchone()
    con.commit()
    con.close()
    return res[0]


def nb_ins_classe_statut(classe, statut):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT ins_num FROM inscriptions WHERE ins_asco=? and ins_classe=? and ins_statut=? """,
                (show_asco_encours(), classe, statut))
    res = cur.fetchall()
    count = 0
    for row in res:
        count += 1

    con.commit()
    con.close()
    return count


def is_inscriptions_exists(elv, matricule):
    asco = show_asco_encours()
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    c.execute("""SELECT * FROM inscriptions WHERE 
                ins_eleve = ? 
                AND ins_matricule LIKE ? 
                AND ins_asco = ?
                ORDER BY ins_num""", (elv, matricule, asco))
    result = c.fetchall()
    conn.commit()
    conn.close()
    return False if result == [] else True


""" Fin des Fonctions de la table inscriptions ________________________________"""

""" 4- Fonctions de la table classes _________________________"""


def all_affectations_by_annee():
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT * FROM affectations WHERE asco = ?""", (show_asco_encours(),))
    res = cur.fetchall()
    final = [
        {'asco': row[1], 'prof': row[2], 'classe': row[3], 'matiere': row[4], 'jour': row[6], 'nb_heures': row[5],
         "creneau": row[7]}
        for row in res
    ]
    con.commit()
    con.close()
    return final


def all_affectations_by_class(classe):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT * FROM affectations WHERE asco = ? AND classe = ?""", (show_asco_encours(), classe))
    res = cur.fetchall()
    con.commit()
    con.close()
    return res


def all_titus_by_annee():
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT * FROM prof_titus WHERE asco = ?""", (show_asco_encours(),))
    res = cur.fetchall()
    con.commit()
    con.close()
    return res


def sel_classe():
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT classe_nom FROM classes""")
    res = cur.fetchall()
    r_final = []
    for row in res:
        r_final.append(row[0])
    con.commit()
    con.close()
    return r_final


def add_class(nom, niv, nomlong, capacite):
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    param = (c.lastrowid, nom, niv, nomlong, capacite)
    c.execute("INSERT INTO classes values (?,?,?,?,?)", param)
    conn.commit()
    conn.close()


def show_classes():
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    c.execute("SELECT classe_nom FROM classes ORDER BY classe_nom")
    resultat = c.fetchall()
    liste2 = []
    conn.commit()
    conn.close()
    for item in resultat:
        liste2.append(item[0])
    return liste2


def show_classes_prim():
    conn = sqlite3.connect(my_base)
    param = ("6E", "5E")
    c = conn.cursor()
    c.execute("SELECT classe_nom FROM classes WHERE niveau LIKE ? or niveau LIKE ? ORDER BY classe_nom", param)
    resultat = c.fetchall()
    liste2 = []
    conn.commit()
    conn.close()
    for item in resultat:
        liste2.append(item[0])
    return liste2


def show_classes_autres():
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    c.execute("SELECT classe_nom, niveau FROM Classes ORDER BY classe_nom")
    resultat = c.fetchall()
    conn.commit()
    conn.close()
    final = [row[0] for row in resultat if "6E" not in row[1] and "5E" not in row[1]]
    return final


def nb_classes():
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    c.execute("SELECT count(classe_nom) FROM classes")
    resultat = c.fetchone()
    conn.commit()
    conn.close()
    return resultat[0]


def search_classe(classe, niveau):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    c = convert_to_like(classe)
    n = convert_to_like(niveau)
    cur.execute("""SELECT id_classe, classe_nom, niveau, class_long, 
                    (SELECT COUNT(ins_num) FROM inscriptions WHERE ins_classe = classes.classe_nom) 
                    FROM Classes 
                    WHERE classe_nom lIKE ?
                    AND niveau LIKE ? 
                    ORDER BY classes.classe_nom""", (c, n))
    res = list(cur.fetchall())
    conn.commit()
    conn.close()
    return res


def update_classe(classe, niv, clong, idclasse):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    param = (classe, niv, clong, idclasse)
    cur.execute("""UPDATE classes SET
                    classe_nom = ?,
                    niveau = ?,
                    class_long = ?
                    WHERE id_classe = ?""", param)
    conn.commit()
    conn.close()


def delete_classe(idclasse):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("DELETE from classes WHERE id_classe =?", (idclasse,))
    conn.commit()
    conn.close()


def classes_sanstitus():
    asco = show_asco_encours()
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT classe_nom FROM Classes LEFT JOIN (SELECT classe FROM prof_titus WHERE asco = ?) AS assignes
                    ON Classes.classe_nom = assignes.classe WHERE assignes.classe IS NULL ORDER BY classe_nom""",
                (asco,))

    resultat = cur.fetchall()
    liste = []
    for res in resultat:
        liste.append(res[0])
    conn.commit()
    conn.close()
    return liste


def niv_fn_classe(classe):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT niveau FROM classes WHERE classe_nom = ?""", (classe,))
    res = cur.fetchone()
    con.commit()
    con.close()
    return res[0]


def show_all_classes():
    conn = sqlite3.connect(my_base)
    asco = show_asco_encours()
    cur = conn.cursor()
    cur.execute("""SELECT id_classe, classe_nom, niveau, class_long, 
                    (SELECT COUNT(ins_num) FROM inscriptions WHERE ins_classe = classes.classe_nom AND ins_asco=?),
                    capacite FROM Classes ORDER BY classes.classe_nom""", (asco,))
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result


def capacite_golbale_classes():
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT sum(capacite) FROM classes""")
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result[0]


def capacite_une_classes(classe):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT capacite FROM classes WHERE classe_nom = ?""", (classe,))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result[0]


def look_nivo(classe):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    param = (classe,)
    cur.execute("""SELECT niveau FROM Classes WHERE classe_nom=?""", param)
    res = cur.fetchone()
    con.commit()
    con.close()
    return res[0]


def is_titus(prof):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    asco = show_asco_encours()
    cur.execute("""SELECT * FROM prof_titus WHERE professeur =? AND asco = ?""", (prof, asco))
    res = cur.fetchone()
    con.commit()
    con.close()
    return True if res is not None else False


""" Fin des Fonctions de la table classes _________________________"""

""" 5- Fonctions de la table professeurs ___________________________"""


def show_all_profs():
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM profs ORDER BY prof_nom""")
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res


def profs_non_titus():
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("""
                    select profs.prof_nom from profs left join 

                    (select professeur from prof_titus where asco = ?) as titus 

                    on profs.prof_nom  = titus.professeur where titus.professeur is Null
                """, (show_asco_encours(),)
                )
    res = cur.fetchall()
    final = [row[0] for row in res]
    conn.commit()
    conn.close()
    return final


def show_nomprof():
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT prof_nom FROM profs ORDER BY prof_nom""")
    res = cur.fetchall()
    liste = []
    for row in res:
        liste.append(row[0])
    conn.commit()
    conn.close()
    return liste


def show_matprof():
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT DISTINCT prof_mat FROM profs ORDER BY prof_mat""")
    res = cur.fetchall()
    liste = []
    for row in res:
        liste.append(row[0])
    conn.commit()
    conn.close()
    return liste


def look_classprof_titus(prof):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    asco = show_asco_encours()
    cur.execute("SELECT classe FROM prof_titus WHERE professeur = ? and asco = ?", (prof, asco))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result[0] if result is not None else "aucun"


def update_prof(nom, sexe, contact, mat, taux, idprof):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    param = (nom, sexe, contact, mat, taux, idprof)
    cur.execute("""UPDATE profs SET
                    prof_nom = ?,
                    prof_sexe = ?,
                    prof_contact = ?,
                    prof_mat = ?
                    taux = ?
                    WHERE id_prof = ?""", param)
    conn.commit()
    conn.close()


def delete_prof(idprof):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    param = (idprof,)
    cur.execute("""DELETE FROM profs WHERE id_prof =? """, param)
    conn.commit()
    conn.close()


def search_prof(prof, mat):
    p = convert_to_like(prof)
    m = convert_to_like(mat)
    param = (p, m)
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("SELECT * FROM profs WHERE prof_nom lIKE ? AND prof_mat LIKE ?", param)
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res


def search_mat_prof(prof):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("SELECT prof_mat FROM profs WHERE prof_nom=?", (prof,))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res[0]


def add_titus(prof, classe, asco):
    param = (prof, classe, asco)
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute(""" INSERT INTO prof_titus values (?,?,?)""", param)
    conn.commit()
    conn.close()


def search_titus(classe):
    asco = show_asco_encours()
    param = (classe, asco)
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute(""" SELECT professeur FROM prof_titus WHERE classe = ? AND asco = ?""", param)
    res = cur.fetchone()
    conn.commit()
    conn.close()
    if res is None:
        resultat = ""
    else:
        resultat = res[0]
    return resultat


def have_titus(classe):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    asco = show_asco_encours()
    cur.execute('SELECT count(professeur) FROM prof_titus WHERE classe = ? AND asco = ?', (classe, asco))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result[0]


def profs_sansclasse():
    asco = show_asco_encours()
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT prof_nom FROM profs LEFT JOIN (SELECT professeur FROM prof_titus WHERE asco =?) AS assignes 
                    ON profs.prof_nom = assignes.professeur WHERE assignes.professeur IS NULL ORDER BY prof_nom""",
                (asco,))
    resultat = cur.fetchall()
    liste = []
    for res in resultat:
        liste.append(res[0])
    conn.commit()
    conn.close()
    return liste


def add_prof(nom, sexe, contact, matiere, taux):
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    param = (c.lastrowid, nom, sexe, contact, matiere, taux)
    c.execute("INSERT INTO profs values (?,?,?,?,?,?)", param)
    conn.commit()
    conn.close()


def add_affectation(prof, classe, matiere, heure, jour, creneau):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    asco = show_asco_encours()
    cur.execute("""INSERT INTO affectations values (?,?,?,?,?,?,?,?)""",
                (cur.lastrowid, asco, prof, classe, matiere, heure, jour, creneau))
    conn.commit()
    conn.close()


def search_prof_affec(classe, matiere):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    asco = show_asco_encours()
    cur.execute("""SELECT prof FROM affectations WHERE asco = ? AND classe = ? AND aff_mat = ?""",
                (asco, classe, matiere))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res[0]


def delete_affectation(prof, classe, aff_mat, jour, creneau):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    asco = show_asco_encours()
    cur.execute("""
                    UPDATE affectations SET nb_heures = ?, 
                    prof = ?, aff_mat = ? WHERE 
                    asco = ? AND prof = ? AND classe = ? AND aff_mat = ? AND
                    jour = ? AND creneau = ?

                    """, (0, '', '', asco, prof, classe, aff_mat, jour, creneau,))
    conn.commit()
    conn.close()


def ajouter_affectation(new_prof, new_aff_mat, classe, jour, creneau):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    asco = show_asco_encours()
    cur.execute("""
                    UPDATE affectations SET nb_heures = ?, 
                    prof = ?,  aff_mat = ? WHERE
                    asco = ? AND classe = ? AND jour = ? AND creneau = ?

                    """, (1, new_prof, new_aff_mat, asco, classe, jour, creneau,))
    conn.commit()
    conn.close()


def is_creneau_prof_oqp(prof, jour, creneau):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    asco = show_asco_encours()
    cur.execute("""SELECT * FROM affectations  WHERE prof = ? AND jour = ? AND creneau = ? AND asco = ?""",
                (prof, jour, creneau, asco))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return True if res is not None else False


def is_creneau_prof_oqp2(prof: str, jour: str, creneau: str):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    asco = show_asco_encours()
    cur.execute("""SELECT * FROM affectations  WHERE prof = ? AND jour = ? AND creneau = ? AND asco = ?""",
                (prof, jour, creneau, asco))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res


def is_creneau_classe_oqp(classe, jour, creneau):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    asco = show_asco_encours()
    cur.execute("""SELECT * FROM affectations  WHERE classe = ? AND jour = ? AND creneau = ? AND asco = ?""",
                (classe, jour, creneau, asco))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return True if res[2] != "" and res[4] != "" else False


# print(is_creneau_classe_oqp("TLE C", "MARDI", "07:30 - 08:30"))


def is_creneau_classe_oqp2(classe, jour, creneau):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    asco = show_asco_encours()
    cur.execute("""SELECT * FROM affectations  WHERE classe = ? AND jour = ? AND creneau = ? AND asco = ?""",
                (classe, jour, creneau, asco))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res


# jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi']
# creneaux = ['07:30 - 08:30', '08:30 - 09:30', '09:30 - 10:30', '10:45 - 11:45', '11:45 - 12:45', '13:00 - 14:00', '14:00 - 15:00', '1500: - 16:00']
#
# for jour in jours:
#     for creneau in creneaux:
#         for classe in show_classes():
#             add_affectation("", classe, "", 0, jour.upper(), creneau)
#             print(classe, jour, creneau)


def is_affec_prof_exists(prof, jour, creneau):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    asco = show_asco_encours()
    cur.execute("""SELECT * FROM affectations WHERE prof = ? and jour = ? and creneau = ? and asco =?""",
                (prof, jour, creneau, asco))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return True if res is not None else False


def is_creneau_occupe(prof, jour, creneau):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    asco = show_asco_encours()
    cur.execute("""SELECT * FROM affectations classe = ? and jour = ? and creneau = ? and asco =?""",
                (prof, jour, creneau, asco))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return True if res is not None else False


def show_all_affectation():
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    asco = show_asco_encours()
    cur.execute("""SELECT * FROM affectations WHERE asco = ?""", (asco,))
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res


def show_affectation_by_prof(prof):
    conn = sqlite3.connect(my_base)
    asco = show_asco_encours()
    cur = conn.cursor()
    cur.execute("""SELECT * FROM affectations WHERE prof = ? AND asco= ?""", (prof, asco))
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res


def unaffected_mat_by_class(niveau, classe):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    asco = show_asco_encours()
    cur.execute("""SELECT matiere FROM (SELECT matiere FROM matieres WHERE mat_niv = ?) AS mat_class

                    LEFT JOIN (
                        SELECT aff_mat FROM affectations WHERE classe = ? AND asco = ?
                    ) AS mat_affectees

                    ON mat_class.matiere = mat_affectees.aff_mat

                    WHERE mat_affectees.aff_mat IS NULL""", (niveau, classe, asco))

    res = cur.fetchall()
    final = [row[0] for row in res]
    conn.commit()
    conn.close()
    return final


def mat_by_class(niveau):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT matiere FROM matieres WHERE mat_niv = ?""", (niveau,))

    res = cur.fetchall()
    final = [row[0] for row in res]
    conn.commit()
    conn.close()
    return final


def profs_fn_type_mat(prof_mat):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT prof_nom FROM profs WHERE prof_mat = ?""", (prof_mat,))
    res = cur.fetchall()
    final = [row[0] for row in res]
    conn.commit()
    conn.close()
    return final


""" Fin des Fonctions de la table professeurs ___________________________"""

""" 6- Fonctions de la table élèves _______________________"""


def show_nom_eleves():
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    c.execute("SELECT nom FROM eleves ORDER BY nom")
    resultat = c.fetchall()
    final = [item[0] for item in resultat]
    conn.commit()
    conn.close()
    return final


def show_nom_eleves_inscrits():
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    c.execute("SELECT ins_eleve FROM inscriptions WHERE ins_asco = ? ORDER BY ins_eleve", (show_asco_encours(),))
    resultat = c.fetchall()
    final = [item[0] for item in resultat]
    conn.commit()
    conn.close()
    return final


def show_all_elev():
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("SELECT * from eleves")
    resultat = cur.fetchall()
    final = [
        {
            'id': data[0], "nom": data[1], "date": data[2], 'lieu': data[3], 'sexe': data[4], 'pere': data[5],
            "mere": data[6], 'contact': data[7], 'matricule': data[8], "image": data[9]
        }
        for data in resultat
    ]
    conn.commit()
    conn.close()
    return final


for row in show_all_elev():
    print(type(row))


def update_nom_elev(matricule, id_elev):
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    c.execute("UPDATE eleves SET nom = ? WHERE id = ?", (matricule, id_elev))
    conn.commit()
    conn.close()


def update_nom_insc(nom, id_ins):
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    c.execute("UPDATE inscriptions SET ins_eleve = ? WHERE ins_num = ?", (nom, id_ins))
    conn.commit()
    conn.close()


def stats_insc_par_classe():
    ascol = show_asco_encours_tuple()
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    c.execute("SELECT ins_classe, COUNT(ins_num) FROM inscriptions WHERE ins_asco = ? GROUP BY ins_classe", ascol)
    resultat = list(c.fetchall())
    conn.commit()
    conn.close()
    return resultat


def update_insc(asco, elev, mat, classe, frais, statut, num):
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    c.execute("""UPDATE inscriptions SET 
        ins_asco = ?, 
        ins_eleve = ?, 
        ins_matricule = ?, 
        ins_classe = ?, 
        ins_frais = ?,
        ins_statut = ?
        WHERE ins_num =?""", (asco, elev, mat, classe, frais, statut, num))
    conn.commit()
    conn.close()


def update_elev(nom, date, lieu, sexe, pere, mere, con, image, id_elev):
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    c.execute("""UPDATE eleves SET
                nom = ?,
                dateN = ?,
                lieuN = ?,
                sexe = ?,
                pere = ?,
                mere = ?,
                contact = ? ,
                image = ?
                WHERE id = ?""", (nom, date, lieu, sexe, pere, mere, con, image, id_elev))
    conn.commit()
    conn.close()


def delete_elev(num):
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    num_t = convert_tuple(num)
    c.execute("DELETE FROM eleves WHERE id = ?", num_t)
    conn.commit()
    conn.close()


def search_matricule(nom):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("SELECT matricule FROM eleves WHERE nom = ? ORDER BY id", (nom,))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result[0]


def search_elev_id(id_elev):
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    c.execute("SELECT * FROM eleves WHERE id=?""", (id_elev,))
    result = c.fetchone()
    conn.commit()
    conn.close()
    return result


def search_elev_by_nom(nom_elev):
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    c.execute("SELECT * FROM eleves WHERE nom=?""", (nom_elev,))
    result = c.fetchone()
    conn.commit()
    conn.close()
    return result


def add_eleve(nom, date, lieu, sexe, pere, mere, contact, matricule, photo):
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    param = (c.lastrowid, nom, date, lieu, sexe, pere, mere, contact, matricule, photo)
    c.execute("INSERT INTO eleves values (?,?,?,?,?,?,?,?,?,?)", param)
    conn.commit()
    conn.close()


def add_sanction(asco, nom, mat, seq, typp, qte):
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    param = (c.lastrowid, asco, nom, mat, seq, typp, qte)
    c.execute("INSERT INTO sanctions values (?,?,?,?,?,?,?)", param)
    conn.commit()
    conn.close()


def all_sanction():
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    c.execute("SELECT * FROM sanctions")
    res = c.fetchall()
    conn.commit()
    conn.close()
    return res


def sanction_by_eleve_seq(nom, sequence, typp):
    conn = sqlite3.connect(my_base)
    asco = show_asco_encours()
    c = conn.cursor()
    c.execute("SELECT sum(qte) FROM sanctions WHERE asco = ? AND nom = ? AND sequence = ? AND type = ?",
              (asco, nom, sequence, typp))
    res = c.fetchone()
    conn.commit()
    conn.close()
    if res[0] is None:
        return 0
    else:
        return res[0]


def sanction_by_eleve_trim(nom, trimestre, typp):
    conn = sqlite3.connect(my_base)
    asco = show_asco_encours()
    c = conn.cursor()
    c.execute("""
        SELECT asco, nom, trimestre, type, sum(qte) FROM (
            SELECT asco, nom, sequence,
            (SELECT trim_nom FROM trimestres WHERE trim_seq = sequence) as trimestre,
            type, qte FROM sanctions
        )
        WHERE asco = ? AND nom = ? AND trimestre = ? AND type = ?
        GROUP BY asco, nom, trimestre, type
    """, (asco, nom, trimestre, typp))
    res = c.fetchone()
    conn.commit()
    conn.close()
    if res is None:
        return 0
    else:
        return res[0]


""" Fin des Fonctions de la table élèves _______________________"""

""" 7- Fonctions de la table pensions ______________________"""


def add_tranche(tranche, montant, pension, asco):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("INSERT INTO tranches VALUES (?,?,?,?,?)", (cur.lastrowid, tranche, montant, pension, asco))
    conn.commit()
    conn.close()


def pension_par_eleve(elv):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    asco = show_asco_encours()
    cur.execute("SELECT * FROM pensions WHERE asco = ? AND elv = ?", (asco, elv))
    res = cur.fetchall()
    final = [
        {'asco': row[1], 'eleve': row[2], 'tranche': row[3], 'montant': row[4], 'date': row[5]} for row in res
    ]
    conn.commit()
    conn.close()
    return final


def global_pension():
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT ins_asco, ins_eleve, ins_classe, 

                    (SELECT verse FROM (SELECT elv, (sum(montant)) as verse FROM pensions WHERE asco = ? GROUP BY elv) WHERE elv = ins_eleve) as montant,

                    (SELECT sum(tranche_mt) FROM tranches WHERE pension = ? and asco = ?) as total

                    FROM inscriptions WHERE ins_asco = ? ORDER BY ins_classe""",
                (show_asco_encours(), "OUI", show_asco_encours(), show_asco_encours()))

    res = cur.fetchall()
    r_final = []

    for row in res:
        if row[3] is None:
            somme = 0
        else:
            somme = row[3]

        reste = row[4] - somme

        if reste == 0:
            statut = 'soldée'
        else:
            statut = 'en cours'

        row = row + (somme, reste, statut)

        r_final.append(row)

    con.commit()
    con.close()
    return r_final


def total_pension():
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    oui = "OUI"
    asco = show_asco_encours()
    cur.execute("SELECT sum(tranche_mt) FROM tranches WHERE pension = ? and asco = ?", (oui, asco))
    res = cur.fetchone()
    con.commit()
    con.close()
    return res[0]


def details_pension(eleve, tranche):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT * FROM pensions WHERE elv =? and tranche=?""", (eleve, tranche))
    res = cur.fetchone()
    con.commit()
    con.close()

    if res is None:
        return 0
    else:
        return res[4]


def search_pension_tranche(tranche):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    asco = show_asco_encours()
    cur.execute("""SELECT ins_asco, ins_eleve, ins_classe, 

                    (SELECT verse FROM (SELECT elv, (sum(montant)) as verse FROM pensions WHERE asco = ? and tranche = ? GROUP BY elv) WHERE elv = ins_eleve) as montant,

                    (SELECT tranche_mt FROM tranches WHERE tranche_nom = ? and asco = ?) as total

                    FROM inscriptions WHERE ins_asco = ?""", (asco, tranche, tranche, asco, asco))

    res = cur.fetchall()
    r_final = []

    for data in res:
        if data[3] is None:
            somme = 0
        else:
            somme = data[3]

        reste = data[4] - somme

        if reste == 0:
            statut = 'soldée'
        else:
            statut = 'en cours'

        new_data = data + (somme, reste, statut)

        r_final.append(new_data)

    con.commit()
    con.close()
    return r_final


def total_tranche(tranche):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    asco = show_asco_encours()
    cur.execute("SELECT tranche_mt FROM tranches WHERE tranche_nom = ? and asco = ?", (tranche, asco))
    res = cur.fetchone()
    con.commit()
    con.close()
    return res[0]


def mt_tranche(tranche):
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    asco = show_asco_encours()
    c.execute("SELECT tranche_mt FROM tranches WHERE tranche_nom =? and asco = ?", (tranche, asco))
    resultat = c.fetchone()
    res = resultat[0]
    conn.commit()
    conn.close()
    return res


def add_pension(asco, elv, tranche, montant, date_p):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    param = (cur.lastrowid, asco, elv, tranche, montant, date_p)
    cur.execute("""INSERT INTO pensions VALUES(?,?,?,?,?, ?)""", param)
    conn.commit()
    conn.close()


def tranche_non_soldee(tranche):
    asco = show_asco_encours()
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute(""" SELECT ins_eleve, ins_asco FROM inscriptions LEFT JOIN 

                     (
                         SELECT elv FROM 

                                (SELECT elv, sum(montant) as p_total FROM pensions 
                                WHERE tranche = ? and asco = ? GROUP BY elv, asco ORDER BY elv)

                            WHERE p_total = (SELECT tranche_mt FROM tranches WHERE tranche_nom = ? and asco = ?)

                    ) AS payes

                     ON inscriptions.ins_eleve = payes.elv WHERE inscriptions.ins_asco = ? AND payes.elv IS NULL
                     """,
                (tranche, asco, tranche, asco, asco))

    res = cur.fetchall()
    r_final = [row[0] for row in res]
    conn.commit()
    conn.close()
    return r_final


def mt_verse_par_tranche_par_eleve(tranche, eleve):
    asco = show_asco_encours()
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT sum(montant) as p_total FROM pensions WHERE tranche = ? and asco = ?
                    AND elv = ?
                    GROUP BY elv, asco""", (tranche, asco, eleve))
    res = cur.fetchone()
    con.commit()
    con.close()
    return res[0] if res is not None else 0


def show_all_pens_t2():
    tranche = 'tranche 2'
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    asco = show_asco_encours()
    cur.execute("""SELECT pens_id, asco, elv, (SELECT ins_classe FROM inscriptions WHERE ins_eleve = pensions.elv AND ins_asco = ?) AS classe, 
                    tranche, montant FROM pensions WHERE tranche =? ORDER BY elv""", (asco, tranche))
    resultat = cur.fetchall()
    conn.commit()
    conn.close()
    return resultat


def show_all_pens_t3():
    tranche = 'tranche 3'
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    asco = show_asco_encours()
    cur.execute("""SELECT pens_id, asco, elv, (SELECT ins_classe FROM inscriptions WHERE ins_eleve = pensions.elv AND ins_asco = ?) AS classe, 
                    tranche, montant FROM pensions WHERE tranche =? ORDER BY elv""", (asco, tranche))
    resultat = cur.fetchall()
    conn.commit()
    conn.close()
    return resultat


def frais_inscription():
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    asco = show_asco_encours()
    tranche = "inscription".upper()
    cur.execute("""SELECT tranche_mt FROM tranches WHERE tranche_nom = ? AND asco = ?""", (tranche, asco))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat[0]


def update_pensions(asco, elv, tranche, montant, idpens):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    param = (asco, elv, tranche, montant, idpens)
    cur.execute(""" UPDATE pensions SET
                    asco = ?,
                    elv = ?,
                    tranche = ?,
                    montant = ?
                    WHERE pens_id = ?""", param)
    conn.commit()
    conn.close()


def delete_pension(idpens):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    param = (idpens,)
    cur.execute("DELETE FROM pensions WHERE pens_id =?", param)
    conn.commit()
    conn.close()


def update_tranche(montant, tranche):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("UPDATE tranches SET tranche_mt = ? WHERE tranche_nom = ?", (montant, tranche))
    conn.commit()
    conn.close()


""" Fin des Fonctions de la table pensions ______________________"""

""" 8- Fonctions de la table trimestres ______________________"""


def trim_fn_seq(seq):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT trim_nom FROM trimestres WHERE trim_seq = ?""", (seq,))
    res = cur.fetchone()
    con.commit()
    con.close()
    return res[0]


def sel_trim():
    con = sqlite3.connect(my_base)
    cur = con.cursor()

    cur.execute("""SELECT DISTINCT trim_nom FROM trimestres""")
    res = cur.fetchall()
    resultat = []
    for t in res:
        resultat.append(t[0])

    con.commit()
    con.close()
    return resultat


def sel_seq():
    con = sqlite3.connect(my_base)
    cur = con.cursor()

    cur.execute("""SELECT DISTINCT trim_seq FROM trimestres""")
    res = cur.fetchall()
    resultat = []
    for t in res:
        resultat.append(t[0])

    con.commit()
    con.close()
    return resultat


def seq_fn_trim(trimestre):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT trim_seq FROM trimestres WHERE trim_nom = ?""", (trimestre,))
    res = cur.fetchall()
    final = [row[0] for row in res]
    con.commit()
    con.close()
    return final


""" Fin des Fonctions de la table trimestres ______________________"""

""" 9- Fonctions de la table utilisateurs _________________________"""


def add_user(nom, poste, acces, login):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""INSERT INTO users values (?,?,?,?,?,?,?)""",
                (cur.lastrowid, nom, poste, acces, login, "", "EN ATTENTE"))
    con.commit()
    con.close()


def delete_user(id_user):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""DELETE FROM users WHERE id = ?""", (id_user,))
    con.commit()
    con.close()


def search_user_state(login):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT etat FROM users WHERE login = ? """, (login,))
    res = cur.fetchone()
    con.commit()
    con.close()
    return res[0] if res is not None else ""


def search_user_infos(login):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT nom, acces, poste, id FROM users WHERE login = ? """, (login,))
    res = cur.fetchone()
    con.commit()
    con.close()
    return res


def search_user_name(name):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    n = "%" + name + "%"
    cur.execute("""SELECT * FROM users WHERE nom LIKE ?""", (n,))
    res = cur.fetchone()
    con.commit()
    con.close()
    return res


def update_user(etat, id_user):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""UPDATE users SET
                    etat = ?
                    WHERE id = ?""", (etat, id_user))

    con.commit()
    con.close()


def update_password_new(password, id_user):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""UPDATE users SET
                    pass = ?
                    WHERE id = ?""", (password, id_user))

    con.commit()
    con.close()


def all_users():
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT * FROM users""")
    res = cur.fetchall()
    con.commit()
    con.close()
    return res


def all_postes():
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT poste FROM droits""")
    res = cur.fetchall()
    final = [row[0] for row in res]
    con.commit()
    con.close()
    return final


def acces_by_poste(poste):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT niveau FROM droits Where poste = ?""", (poste,))
    res = cur.fetchone()
    con.commit()
    con.close()
    return res[0]


def infos_user(login):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT nom, acces FROM users WHERE login = ?""", (login,))
    res = cur.fetchone()
    con.commit()
    con.close()
    return res if res is not None else False


def user_exists(login, mdp):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    couple = (login, mdp)
    cur.execute("""SELECT login, pass FROM users""")
    res = cur.fetchall()
    count = 0

    for tup in res:
        if couple == tup:
            count += 1

    con.commit()
    con.close()
    return True if count > 0 else False


def niveau_acces(login):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT acces FROM users WHERE login =?""", (login,))
    res = cur.fetchone()
    con.commit()
    con.close()
    return res[0]


""" Fin des Fonctions de la table utilisateurs _________________________"""

""" 10- Fonctions de la table niveaux _____________________________"""


def add_niveau(nom, exam, name_exam, serie, nom_long, cycle, section):
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    param = (c.lastrowid, nom, exam, name_exam, serie, nom_long, cycle, section)
    c.execute("INSERT INTO niveaux values (?,?,?,?,?,?,?,?)", param)
    conn.commit()
    conn.close()


def niveaux():
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("SELECT niv_nom FROM niveaux ORDER BY niv_nom")
    liste = []
    result = cur.fetchall()
    for res in result:
        liste.append(res[0])
    conn.commit()
    conn.close()
    return liste


def cycle_par_niveau(niveau):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("SELECT cycle FROM niveaux WHERE niv_nom = ?", (niveau,))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result[0]


def all_niveaux_by_section_cyle(section, cycle):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("SELECT niv_nom FROM niveaux WHERE section = ? AND cycle = ?", (section, cycle,))
    result = cur.fetchall()
    final = [row[0] for row in result]
    conn.commit()
    conn.close()
    return final


def show_all_niveaux():
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM niveaux ORDER BY niv_id""")
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res


def search_niveau(nivo):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    param = (nivo,)
    cur.execute("SELECT * FROM niveaux WHERE niv_nom LIKE ? ", param)
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res


def delete_niveau(idniv):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    param = (idniv,)
    cur.execute("DELETE FROM niveaux WHERE niv_id = ? ", param)
    conn.commit()
    conn.close()


def update_niveau(nom, exam, examname, serie, nom_long, idniv):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    param = (nom, exam, examname, serie, nom_long, idniv)
    cur.execute("""UPDATE niveaux SET
                niv_nom = ?,
                niv_exam = ?,
                niv_name_exam = ?,
                niv_serie = ?,
                niv_long = ?
                WHERE niv_id = ?""", param)
    conn.commit()
    conn.close()


""" Fin des Fonctions de la table niveaux _____________________________"""

""" 11- Fonctions de la table matieres ____________________"""


def matieres_fn_niv(niveau):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT matiere FROM Matieres  WHERE mat_niv =?""", (niveau,))
    res = cur.fetchall()
    r_final = []
    for r in res:
        r_final.append(r[0])
    con.commit()
    con.close()
    return r_final


def aal_matieres():
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT * FROM Matieres""")
    res = cur.fetchall()
    con.commit()
    con.close()
    return res


def update_nom_matiere(mat, id_mat):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""UPDATE Matiere SET matiere = ? WHERE id_mat = ?""", (mat, id_mat))
    con.commit()
    con.close()


def coef_fn_mat_niv(matiere, niveau):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT mat_coeff FROM Matieres  WHERE matiere =? and mat_niv =?""", (matiere, niveau,))
    res = cur.fetchone()
    con.commit()
    con.close()
    return res[0]


def add_matiere(mat, group, typ, niv, cof, heures, dim):
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    param = (c.lastrowid, mat, group, typ, niv, cof, heures, dim)
    c.execute("INSERT INTO Matieres values (?,?,?,?,?,?,?,?)", param)
    conn.commit()
    conn.close()


def charge_horaire_by_mat_nivo(nivo, mat):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    param = (nivo, mat)
    cur.execute("SELECT nb_heures FROM Matieres WHERE mat_niv = ? and matiere = ?", param)
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res[0]


def dim_by_nivo(nivo, mat):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    param = (nivo, mat)
    cur.execute("SELECT dim FROM Matieres WHERE mat_niv = ? and matiere = ?", param)
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res[0] if res is not None else ""


# file = "MATIERES.xlsx"
# absolute_path = os.path.abspath(file)
# workbook = openpyxl.load_workbook(absolute_path)
# sheet = workbook.active
# valeurs = list(sheet.values)
# header = valeurs[0]
# valeurs.remove(header)
#
# for item in valeurs:
#     add_matiere(item[0], item[1], item[2], item[3], item[4], item[5], item[6])
#     print(item[0], item[1], item[2], item[3], item[4], item[5])


def show_typemat():
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT type FROM  Matieres ORDER BY type")
    result = cur.fetchall()
    r_final = []

    for res in result:
        r_final.append(res[0])

    conn.commit()
    conn.close()
    return r_final


def show_matieres():
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT matiere FROM matieres ORDER BY matiere")
    result = cur.fetchall()
    resultat = []

    for res in result:
        resultat.append(res[0])

    conn.commit()
    conn.close()
    return resultat


def show_matieres_fn_niv(niveau):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("select DISTINCT matiere FROM Matieres WHERE mat_niv = ? ORDER BY matiere", (niveau,))
    result = cur.fetchall()
    resultat = []

    for res in result:
        resultat.append(res[0])

    conn.commit()
    conn.close()
    return resultat


def del_mat():
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""DELETE FROM Matieres""")
    con.commit()
    con.close()


def show_all_matieres():
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM Matieres ORDER BY id_mat""")
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res


def show_mat():
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT DISTINCT matiere FROM Matieres ORDER BY matiere""")
    res = cur.fetchall()
    liste = []
    for i in res:
        liste.append(i[0])
    conn.commit()
    conn.close()
    return liste


def search_mat(mat, niv):
    m = convert_to_like(mat)
    n = convert_to_like(niv)
    param = (m, n)
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * s WHERE 
                    matiere LIKE ?
                    AND mat_niv LIKE ? 
                    ORDER BY id_mat""", param)
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res


def update_mat(mat, grp, typ, niv, coeff, idmat):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    param = (mat, grp, typ, niv, coeff, idmat)
    cur.execute("""UPDATE Matiere SET
                    matiere = ?,
                    groupe = ?, 
                    type = ?,
                    mat_niv = ?,
                    mat_coeff = ?
                    WHERE id_mat = ?""", param)
    conn.commit()
    conn.close()


def delete_matiere(idmat):
    param = (idmat,)
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("""DELETE FROM Matieres WHERE id_mat = ?""", param)
    conn.commit()
    conn.close()


def show_mat_fn_nivo(nivo):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    param = (nivo,)
    cur.execute("SELECT * FROM Matieres WHERE mat_niv = ? ", param)
    res = cur.fetchall()
    conn.commit()
    conn.close()
    return res


def type_fn_mat(matiere):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT type FROM matieres WHERE matiere = ? AND mat_niv""", (matiere,))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res[0] if res is not None else ""


def nb_heures_par_matiere(matiere, nivo):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("SELECT nb_heures FROM Matieres WHERE matiere = ? AND mat_niv = ? ", (matiere, nivo))
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res[0] if res is not None else ""


""" Fin des Fonctions de la table matieres ____________________"""

""" 12- Fonctions de la table notes _____________________________"""


def add_notes(nom, asco, seq, classe, mat, coef, note, user):
    conn = sqlite3.connect(my_base)
    heure = datetime.datetime.now()
    c = conn.cursor()
    param = (c.lastrowid, nom, asco, seq, classe, mat, coef, note, heure, heure, user)

    c.execute("INSERT INTO notes values (?,?,?,?,?,?,?,?,?,?,?)", param)

    conn.commit()
    conn.close()


def show_all_notes():
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT *
                    FROM NOTES WHERE asco = ?""", (show_asco_encours(),))
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result


def show_all_notes_prim():
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT *
                    FROM notes_prim WHERE asco = ?""", (show_asco_encours(),))
    result = cur.fetchall()
    conn.commit()
    conn.close()
    return result


def search_notes(classe, nom, matiere, sequence):
    c = convert_to_like(classe)
    n = convert_to_like(nom)
    m = convert_to_like(matiere)
    s = convert_to_like(sequence)
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM NOTES WHERE asco LIKE ?
                    AND classe LIKE ?
                    AND nom LIKE ?
                    AND matiere LIKE ?
                    AND sequence LIKE? """, (show_asco_encours(), c, n, m, s))
    result = list(cur.fetchall())
    conn.commit()
    conn.close()
    return result


def search_note_id(id_note):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM NOTES WHERE asco LIKE ?
                    AND id =?""", (show_asco_encours(), id_note))
    result = cur.fetchone()
    conn.commit()
    conn.close()
    return result


def update_notes(note, idnote, user):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    last_modified = datetime.datetime.now()
    param = (note, last_modified, user, idnote)
    cur.execute("""UPDATE notes SET

                note = ?,
                last_modified = ?,
                user = ?
                WHERE id = ?""", param)

    conn.commit()
    conn.close()


def delete_notes(idnote):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("DELETE from notes WHERE id =?", (idnote,))
    conn.commit()
    conn.close()


def eleves_sans_note(classe, sequence, matiere, classe_2):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    asco = show_asco_encours()
    cur.execute("""SELECT ins_eleve FROM (SELECT ins_eleve, ins_asco FROM inscriptions WHERE ins_classe = ? AND ins_asco = ?) as inscrits_classe
                    LEFT JOIN (
                        SELECT Notes.nom FROM Notes WHERE Notes.asco = ?
                        AND Notes.sequence = ?
                        AND Notes.matiere = ?
                        AND Notes.classe = ?) AS have_a_note

                    ON inscrits_classe.ins_eleve = have_a_note.nom 
                    WHERE have_a_note.nom IS NULL ORDER BY inscrits_classe.ins_eleve """,
                (classe, asco, asco, sequence, matiere, classe_2)
                )
    res = cur.fetchall()
    final = [row[0] for row in res]
    conn.commit()
    conn.close()
    return final


def del_notes():
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("""DELETE FROM Notes""")
    conn.commit()
    conn.close()


def search_note_from_id(idnote):
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM Notes WHERE id =?""", (idnote,))
    resultat = cur.fetchone()
    conn.commit()
    conn.close()
    return resultat


""" Fin des Fonctions de la table notes _____________________________"""

""" 13- bulletins sequentiels _______________________________"""


def moygen_seq():
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    asco = show_asco_encours()
    cur.execute("""SELECT classe, sequence, avg(moyenne) as moygen
        FROM 
        (SELECT asco, classe, nom, 
        (SELECT trim_nom FROM trimestres WHERE trim_seq = Notes.sequence) AS trimestre,
        sequence, sum(coeff) as coef, 

        (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,
        (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,

        sum((coeff*note)) AS nc, (sum(coeff*note)/sum(coeff))as moyenne 

        FROM Notes where asco=?

        GROUP BY nom, sequence ORDER BY classe, sequence, moyenne DESC)

        GROUP BY classe, sequence ORDER BY classe, sequence""", (asco, asco))

    res = cur.fetchall()

    conn.commit()
    conn.close()
    return res


def bull_seq():
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    param = (show_asco_encours(), show_asco_encours())
    cur.execute("""SELECT asco, classe,

                (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,
                sequence, nom, 

                (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                sum((coeff*note)) AS nc, sum(coeff) as coef,  (sum(coeff*note)/sum(coeff))as moyenne 

                FROM Notes Where asco=?
                GROUP BY nom, sequence ORDER BY classe, sequence, moyenne DESC""", param)

    res = cur.fetchall()
    r_final = []

    for row in res:
        i = 0
        count = 0
        while i < len(res):
            if res[i][1] == row[1] and res[i][3] == row[3]:
                if res[i][8] > row[8]:
                    count += 1
                else:
                    count = count
            else:
                count = count
            i += 1

        rang = count + 1

        new_row = row + (rang,)
        r_final.append(new_row)

    con.commit()
    con.close()
    return r_final


def bull_seq_class_seq(classe, sequence):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    param = (show_asco_encours(), show_asco_encours(), classe, sequence)
    cur.execute("""SELECT asco, classe,

                (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,
                sequence, nom, 

                (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                sum((coeff*note)) AS nc, sum(coeff) as coef,  (sum(coeff*note)/sum(coeff))as moyenne 

                FROM Notes Where asco=? AND classe = ? AND sequence = ?
                GROUP BY nom, sequence ORDER BY classe, sequence, moyenne DESC""", param)

    res = cur.fetchall()
    r_final = []

    for row in res:
        i = 0
        count = 0
        while i < len(res):
            if res[i][1] == row[1] and res[i][3] == row[3]:
                if res[i][8] > row[8]:
                    count += 1
                else:
                    count = count
            else:
                count = count
            i += 1

        rang = count + 1

        new_row = row + (rang,)
        r_final.append(new_row)

    con.commit()
    con.close()
    return r_final


def effectif_classe(classe):
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    asco = show_asco_encours()
    param = (asco, classe)
    c.execute("SELECT COUNT(ins_num) from inscriptions WHERE ins_asco = ? AND ins_classe = ?", param)
    resultat = c.fetchone()
    conn.commit()
    conn.close()
    return resultat[0] if resultat is not None else 0


def search_moygen(classe, sequence):
    conn = sqlite3.connect(my_base)
    c = conn.cursor()
    asco = show_asco_encours()
    param = (asco, classe, sequence)
    c.execute("""SELECT classe, sequence, avg(moyenne) as moygen

                FROM (SELECT asco, classe, nom, 
                (SELECT trim_nom FROM trimestres WHERE trim_seq = Notes.sequence) AS trimestre,
                sequence, sum(coeff) as coef, 
                (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,
                (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,
                sum((coeff*note)) AS nc, (sum(coeff*note)/sum(coeff))as moyenne 
                FROM Notes GROUP BY nom, sequence ORDER BY classe, sequence, moyenne DESC)

                WHERE classe = ? AND sequence = ?
                GROUP BY classe, sequence ORDER BY classe, sequence""", param)

    resultat = c.fetchone()
    conn.commit()
    conn.close()
    return resultat[2] if resultat is not None else 0


def search_notemin_seq(classe, sequence):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    param = (show_asco_encours(), classe, sequence)
    cur.execute("""SELECT asco, classe,

                (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,
                sequence, nom, 

                (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                sum((coeff*note)) AS nc, sum(coeff) as coef,  (sum(coeff*note)/sum(coeff))as moyenne 

                FROM Notes WHERE classe = ? AND sequence =?
                GROUP BY nom, sequence ORDER BY classe, sequence, moyenne""", param)

    res = cur.fetchone()
    con.commit()
    con.close()
    return res[8] if res is not None else 0


def search_notemax_seq(classe, sequence):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    param = (show_asco_encours(), classe, sequence)
    cur.execute("""SELECT asco, classe,

                (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,
                sequence, nom, 

                (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                sum((coeff*note)) AS nc, sum(coeff) as coef,  (sum(coeff*note)/sum(coeff))as moyenne 

                FROM Notes WHERE classe = ? AND sequence =?
                GROUP BY nom, sequence ORDER BY classe, sequence, moyenne DESC""", param)

    res = cur.fetchone()
    con.commit()
    con.close()
    return res[8] if res is not None else 0


def nb_admis_seq(classe, sequence):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    param = (show_asco_encours(), classe, sequence)
    cur.execute("""SELECT asco, classe,

                (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,
                sequence, nom, 

                (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                sum((coeff*note)) AS nc, sum(coeff) as coef,  (sum(coeff*note)/sum(coeff))as moyenne 

                FROM Notes WHERE classe = ? AND sequence =?
                GROUP BY nom, sequence ORDER BY classe, sequence, moyenne""", param)

    res = cur.fetchall()
    count = 0
    for row in res:
        if float(row[8]) >= 10:
            count += 1
        else:
            count = count

    con.commit()
    con.close()
    return count


def search_bull_seq(classe, sequence):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    c = convert_to_like(classe)
    s = convert_to_like(sequence)
    param = (show_asco_encours(), show_asco_encours(), c, s)
    cur.execute("""SELECT asco, classe,

                (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,
                sequence, nom, 

                (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                sum((coeff*note)) AS nc, sum(coeff) as coef,  (sum(coeff*note)/sum(coeff))as moyenne 

                FROM Notes WHERE asco=? AND classe LIKE ? AND sequence LIKE ?
                GROUP BY nom, sequence ORDER BY classe, sequence, moyenne DESC""", param)

    res = cur.fetchall()
    r_final = []

    for row in res:
        i = 0
        count = 0
        while i < len(res):
            if res[i][1] == row[1] and res[i][3] == row[3]:
                if res[i][8] > row[8]:
                    count += 1
                else:
                    count = count
            else:
                count = count
            i += 1

        rang = count + 1

        row = row + (rang,)
        r_final.append(row)

    con.commit()
    con.close()
    return r_final


def details_notes(classe, sequence, eleve):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    asco = show_asco_encours()
    param = (asco, classe, sequence, eleve)
    cur.execute(""" SELECT nom, matiere, coeff, note, (coeff*note)as total
                    FROM Notes WHERE asco =? AND classe=? AND sequence  =? AND nom =?""", param)
    res = cur.fetchall()
    r_final = []

    for row in res:
        apprec = trouver_cote(row[3])

        row = row + (apprec,)
        r_final.append(row)

    con.commit()
    con.close()
    return r_final


def details_notes_groupe(classe, sequence, eleve):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    asco = show_asco_encours()
    param = (asco, classe, sequence, eleve)
    cur.execute(""" SELECT matiere,

                    (SELECT niveau FROM Classes WHERE classe_nom = classe) as nivo, coeff, note,

                    (note * coeff) as totaux,

                    (SELECT groupe FROM matieres WHERE mat_niv = (SELECT niveau FROM Classes WHERE classe_nom = classe) AND matiere = notes.matiere) as groupe

                    FROM notes WHERE asco =? AND classe=? AND sequence  =? AND nom =?""", param)

    res = cur.fetchall()
    r_final = []

    for row in res:
        apprec = trouver_cote(row[3])

        row = row + (apprec,)
        r_final.append(row)

    con.commit()
    con.close()
    return r_final


def search_te_seq(classe, sequence):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    param = (show_asco_encours(), classe, sequence)
    cur.execute("""SELECT asco, classe,

                (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,
                sequence, nom, 

                (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                sum((coeff*note)) AS nc, sum(coeff) as coef,  (sum(coeff*note)/sum(coeff))as moyenne 

                FROM Notes WHERE classe = ? AND sequence =?
                GROUP BY nom, sequence ORDER BY classe, sequence, moyenne""", param)

    res = cur.fetchall()
    a = 0

    count = 0
    for row in res:
        if float(row[8]) < 10:
            count += 1
        else:
            count = count
        a += 1

    resultat = f"{(float(count / a) * 100):.2f}%"
    con.commit()
    con.close()
    return resultat


def search_tr_seq(classe, sequence):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    param = (show_asco_encours(), classe, sequence)
    cur.execute("""SELECT asco, classe,

                (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,
                sequence, nom, 

                (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                sum((coeff*note)) AS nc, sum(coeff) as coef,  (sum(coeff*note)/sum(coeff))as moyenne 

                FROM Notes WHERE classe = ? AND sequence =?
                GROUP BY nom, sequence ORDER BY classe, sequence, moyenne""", param)

    res = cur.fetchall()
    a = 0
    count = 0
    for row in res:
        if float(row[8]) >= 10.0:
            count += 1
        else:
            count = count
        a += 1

    resultat = f"{(float(count / a) * 100):.2f} %"
    con.commit()
    con.close()
    return resultat


# fonctions qui permetent de récupérer les notes séquentielles d'un élève
def note_sequentielle_par_matiere(nom, seq, mat):
    asco = show_asco_encours()
    param = (asco, nom, seq, mat)
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT asco, classe, sequence,

                    nom, matiere, coeff, note

                    FROM Notes WHERE asco=? AND nom=? AND sequence = ? AND matiere =?

                    """, param)

    res = cur.fetchone()
    con.commit()
    con.close()
    return res[6]


def note_min_mat_seq(matiere, sequence, classe):
    asco = show_asco_encours()
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT min(note)FROM Notes WHERE
        notes.matiere = ? AND notes.sequence = ? AND notes.asco = ? AND notes.classe = ?
        """, (matiere, sequence, asco, classe)
    )
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res[0]


def note_min_mat_trim(classe, matiere, trimestre):
    asco = show_asco_encours()
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT min(new_note) FROM (
            SELECT nom, matiere, avg(note) as new_note, trimetre FROM (
                SELECT asco, nom, sequence, 
                (select trim_nom from trimestres where trim_seq = sequence) as trimetre,
                classe, matiere, coeff, note FROM Notes WHERE asco = ? AND classe = ? AND matiere = ?
            )
            WHERE trimetre = ? GROUP BY nom, matiere, trimetre	
        )
        """, (asco, classe, matiere, trimestre)
    )
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res[0]


def note_max_mat_trim(classe, matiere, trimestre):
    asco = show_asco_encours()
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT max(new_note) FROM (
            SELECT nom, matiere, avg(note) as new_note, trimetre FROM (
                SELECT asco, nom, sequence, 
                (select trim_nom from trimestres where trim_seq = sequence) as trimetre,
                classe, matiere, coeff, note FROM Notes WHERE asco = ? AND classe = ? AND matiere = ?
            )
            WHERE trimetre = ? GROUP BY nom, matiere, trimetre	
        )
        """, (asco, classe, matiere, trimestre)
    )
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res[0]


def note_max_mat_seq(matiere, sequence, classe):
    asco = show_asco_encours()
    conn = sqlite3.connect(my_base)
    cur = conn.cursor()
    cur.execute(
        """
            SELECT max(note)FROM Notes WHERE notes.matiere = ? 
            AND notes.sequence = ? AND notes.asco = ? AND classe = ? """, (matiere, sequence, asco, classe)
    )
    res = cur.fetchone()
    conn.commit()
    conn.close()
    return res[0]


""" Fin des fonctions bulletins sequentiels _______________________________"""

""" 14- Fonction des bulletins trimestriels _______________________________"""


def bull_trim():
    asco = show_asco_encours()
    param = (asco, asco)
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT asco, classe,

                    (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,

                    (SELECT trim_nom FROM trimestres WHERE trimestres.trim_seq = notes.sequence) as trimestre,

                    nom,

                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                    sum((coeff*note)) AS nc, sum(coeff) as coef,  

                    (sum(coeff*note)/sum(coeff)) as moyenne 

                    FROM Notes WHERE asco=?

                    GROUP BY asco, nom, trimestre  ORDER BY classe, trimestre, nom, moyenne DESC""", param)

    res = cur.fetchall()
    r_final = []

    for row in res:
        i = 0
        count = 0
        while i < len(res):
            if res[i][1] == row[1] and res[i][3] == row[3]:
                if res[i][8] > row[8]:
                    count += 1
                else:
                    count = count
            else:
                count = count
            i += 1

        rang = count + 1

        row = row + (rang,)
        r_final.append(row)

    con.commit()
    con.close()
    return r_final


def bull_trim_classe_trim(classe, sequence):
    asco = show_asco_encours()
    param = (asco, asco, classe, sequence)
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT asco, classe,

                    (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,

                    (SELECT trim_nom FROM trimestres WHERE trimestres.trim_seq = notes.sequence) as trimestre,

                    nom,

                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                    sum((coeff*note)) AS nc, sum(coeff) as coef,  

                    (sum(coeff*note)/sum(coeff)) as moyenne 

                    FROM Notes WHERE asco=? AND classe = ? AND trimestre = ?

                    GROUP BY asco, nom, trimestre  ORDER BY classe, trimestre, nom, moyenne DESC""", param)

    res = cur.fetchall()
    r_final = []

    for row in res:
        i = 0
        count = 0
        while i < len(res):
            if res[i][1] == row[1] and res[i][3] == row[3]:
                if res[i][8] > row[8]:
                    count += 1
                else:
                    count = count
            else:
                count = count
            i += 1

        rang = count + 1

        row = row + (rang,)
        r_final.append(row)

    con.commit()
    con.close()
    return r_final


# def bull_trim():
#     asco = show_asco_encours()
#     param = (asco, asco)
#     con = sqlite3.connect(my_base)
#     cur = con.cursor()
#     cur.execute("""SELECT asco,
#
#                     classe,
#
#                     (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,
#
#                     (SELECT trim_nom FROM trimestres WHERE trimestres.trim_seq = notes.sequence) as trimestre,
#
#                     nom,
#
#                     (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,
#
#                     sum((coeff*note)) AS nc,
#
#                     sum(coeff) as coef,
#
#                     (sum(coeff*note)/sum(coeff)) as moyenne
#
#                     FROM Notes WHERE asco=?
#
#                     GROUP BY asco, nom, trimestre  ORDER BY classe, trimestre, nom, moyenne DESC""", param)
#
#     res = cur.fetchall()
#     r_final = []
#
#     for row in res:
#         i = 0
#         count = 0
#         while i < len(res):
#             if res[i][1] == row[1] and res[i][3] == row[3]:
#                 if res[i][8] > row[8]:
#                     count += 1
#                 else:
#                     count = count
#             else:
#                 count = count
#             i += 1
#
#         rang = count + 1
#
#         row = row + (rang,)
#         r_final.append(row)
#
#     con.commit()
#     con.close()
#     return r_final


def search_bull_trim(classe, trimestre):
    c = convert_to_like(classe)
    t = convert_to_like(trimestre)
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    param = (show_asco_encours(), show_asco_encours(), c, t)
    cur.execute("""SELECT asco, classe,

                    (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,

                    (SELECT trim_nom FROM trimestres WHERE trimestres.trim_seq = notes.sequence) as trimestre,

                    nom,

                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                    sum((coeff*note)) AS nc, sum(coeff) as coef,  

                    (sum(coeff*note)/sum(coeff)) as moyenne 

                    FROM Notes WHERE asco=? AND classe LIKE? AND trimestre LIKE?

                    GROUP BY asco, nom, trimestre  ORDER BY classe, trimestre, nom, moyenne DESC""", param)

    res = cur.fetchall()
    r_final = []

    for row in res:
        i = 0
        count = 0
        while i < len(res):
            if res[i][1] == row[1] and res[i][3] == row[3]:
                if res[i][8] > row[8]:
                    count += 1
                else:
                    count = count
            else:
                count = count
            i += 1

        rang = count + 1

        row = row + (rang,)
        r_final.append(row)

    con.commit()
    con.close()
    return r_final


def detail_bull_trim(classe, trimestre, nom):
    asco = show_asco_encours()
    param = (asco, asco, classe, trimestre, nom)
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT asco, classe,
                    (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,
                    (SELECT trim_nom FROM trimestres WHERE trimestres.trim_seq = notes.sequence) as trimestre,
                    nom, matiere,
                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,
                    avg(note) AS nc, avg(coeff) as coef, (avg(note)*avg(coeff)) as total,
                    (SELECT groupe FROM matieres WHERE mat_niv = (SELECT niveau FROM Classes WHERE classe_nom = classe) AND matiere = notes.matiere) as groupe
                    FROM Notes WHERE asco =? AND classe=? AND trimestre=? AND nom=?
                    GROUP BY asco, nom, trimestre, matiere  ORDER BY trimestre, classe, nom, matiere, total DESC""",
                param)

    res = cur.fetchall()
    r_final = []

    for row in res:
        apprec = trouver_cote(row[7])

        new_row = row + (apprec,)
        r_final.append(new_row)

    last = [
        {
            "asco": row[0], "classe": row[1], "trimestre": row[3], "nom": row[4], "matiere": row[5],
            "note": row[7], "coeff": row[8], "total": row[9], "cote": row[11], "groupe": row[10]
        }
        for row in r_final
    ]

    con.commit()
    con.close()
    return last


def moygen_trim(classe, trimestre):
    asco = show_asco_encours()
    param = (asco, asco, classe, trimestre)
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT classe, trimestre, avg(moyenne) as moygen

                        FROM (SELECT asco, classe,

                        (SELECT trim_nom FROM trimestres WHERE trimestres.trim_seq = notes.sequence) as trimestre,

                        nom,

                        sum((coeff*note)) AS nc, sum(coeff) as coef,  (sum(coeff*note)/sum(coeff))as moyenne 

                        FROM Notes where asco = ?

                        GROUP BY asco, nom, trimestre  ORDER BY classe, nom, moyenne DESC)

                        WHERE asco=? AND classe=? AND trimestre=?

                        GROUP BY classe, trimestre ORDER BY asco, classe, trimestre""", param)

    res = cur.fetchone()
    con.commit()
    con.close()
    return res[2]


def notemin_trim(classe, trimestre):
    asco = show_asco_encours()
    param = (asco, asco, classe, trimestre)
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT asco, classe,

                    (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,

                    (SELECT trim_nom FROM trimestres WHERE trimestres.trim_seq = notes.sequence) as trimestre,

                    nom,

                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                    sum((coeff*note)) AS nc, sum(coeff) as coef,  (sum(coeff*note)/sum(coeff))as moyenne 

                    FROM Notes WHERE asco=? AND classe=? AND trimestre=?

                    GROUP BY asco, nom, trimestre  ORDER BY classe, moyenne, nom""", param)

    res = cur.fetchone()
    con.commit()
    con.close()
    return res[8]


def notemax_trim(classe, trimestre):
    asco = show_asco_encours()
    param = (asco, asco, classe, trimestre)
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT asco, classe,

                    (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,

                    (SELECT trim_nom FROM trimestres WHERE trimestres.trim_seq = notes.sequence) as trimestre,

                    nom,

                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                    sum((coeff*note)) AS nc, sum(coeff) as coef,  (sum(coeff*note)/sum(coeff))as moyenne 

                    FROM Notes WHERE asco=? AND classe=? AND trimestre=?

                    GROUP BY asco, nom, trimestre  ORDER BY classe, moyenne DESC, nom""", param)

    res = cur.fetchone()
    con.commit()
    con.close()
    return res[8]


def tr_trim(classe, trimestre):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    param = (show_asco_encours(), show_asco_encours(), classe, trimestre)
    cur.execute("""SELECT asco, classe,

                    (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,

                    (SELECT trim_nom FROM trimestres WHERE trimestres.trim_seq = notes.sequence) as trimestre,

                    nom,

                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                    sum((coeff*note)) AS nc, sum(coeff) as coef,  (sum(coeff*note)/sum(coeff))as moyenne 

                    FROM Notes WHERE asco=? AND classe=? AND trimestre=?

                    GROUP BY asco, nom, trimestre  ORDER BY classe, nom, moyenne DESC""", param)

    res = cur.fetchall()
    a = effectif_classe(classe)
    count = 0
    for row in res:
        if float(row[8]) >= 10.0:
            count += 1
        else:
            count = count
    resultat = f"{(float(count / a) * 100):.2f}%"
    con.commit()
    con.close()
    return resultat


def te_trim(classe, trimestre):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    param = (show_asco_encours(), show_asco_encours(), classe, trimestre)
    cur.execute("""SELECT asco, classe,

                    (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,

                    (SELECT trim_nom FROM trimestres WHERE trimestres.trim_seq = notes.sequence) as trimestre,

                    nom,

                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                    sum((coeff*note)) AS nc, sum(coeff) as coef,  (sum(coeff*note)/sum(coeff))as moyenne 

                    FROM Notes WHERE asco=? AND classe=? AND trimestre=?

                    GROUP BY asco, nom, trimestre  ORDER BY classe, nom, moyenne DESC""", param)

    res = cur.fetchall()
    a = effectif_classe(classe)
    count = 0
    for row in res:
        if float(row[8]) < 10.0:
            count += 1
        else:
            count = count
    resultat = f"{(float(count / a) * 100):.2f}%"
    con.commit()
    con.close()
    return resultat


def nb_admis_trim(classe, trimestre):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    param = (show_asco_encours(), show_asco_encours(), classe, trimestre)
    cur.execute("""SELECT asco, classe,

                    (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,

                    (SELECT trim_nom FROM trimestres WHERE trimestres.trim_seq = notes.sequence) as trimestre,

                    nom,

                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                    sum((coeff*note)) AS nc, sum(coeff) as coef,  (sum(coeff*note)/sum(coeff)) as moyenne 

                    FROM Notes WHERE asco=? AND classe=? AND trimestre=?

                    GROUP BY asco, nom, trimestre  ORDER BY classe, nom, moyenne DESC""", param)

    res = cur.fetchall()
    count = 0
    for row in res:
        if float(row[8]) >= 10:
            count += 1
        else:
            count = count

    con.commit()
    con.close()
    return count


def rech_bull_seq(seq, nom):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    param = (show_asco_encours(), seq, nom)
    cur.execute("""SELECT asco, classe,

                (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,
                sequence, nom,

                sum((coeff*note)) AS nc, sum(coeff) as coef,  (sum(coeff*note)/sum(coeff))as moyenne 

                FROM Notes Where asco=? AND  sequence =? AND nom=?
                GROUP BY nom, sequence ORDER BY classe, sequence, moyenne DESC""", param)

    res = cur.fetchone()
    con.commit()
    con.close()
    return res[7]


def notes_groupe_trim(classe, nom, trim):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    asco = show_asco_encours()
    param = (asco, asco, classe, nom, trim)

    cur.execute("""SELECT asco, classe,

                    (SELECT trim_nom FROM trimestres WHERE trimestres.trim_seq = notes.sequence) as trimestre,

                    nom, matiere,

                    (SELECT groupe FROM matieres WHERE mat_niv = (SELECT niveau FROM Classes WHERE classe_nom = classe) AND matiere = notes.matiere) as groupe,

                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                    avg(note) AS nc, avg(coeff) as coef,  (avg(note)*avg(coeff))as total

                    FROM Notes WHERE asco =?  AND classe =? AND nom=? AND trimestre =?

                    GROUP BY asco, nom, trimestre, matiere  ORDER BY trimestre, classe, nom, matiere, total DESC""",
                param)

    res = cur.fetchall()
    r_final = []

    for row in res:
        apprec = trouver_cote(row[7])

        new_row = row + (apprec,)
        r_final.append(new_row)

    con.commit()
    con.close()
    return r_final


def notes_sup_moygen_trim(classe, trimestre):
    asco = show_asco_encours()
    param = (asco, asco, classe, trimestre)
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT classe, nom, trimestre, avg(moyenne) as moygen

                        FROM (SELECT asco, classe,

                        (SELECT trim_nom FROM trimestres WHERE trimestres.trim_seq = notes.sequence) as trimestre,

                        nom,

                        sum((coeff*note)) AS nc, sum(coeff) as coef,  (sum(coeff*note)/sum(coeff))as moyenne 

                        FROM Notes where asco = ?

                        GROUP BY asco, nom, trimestre  ORDER BY classe, nom, moyenne DESC)

                        WHERE asco=? AND classe=? AND trimestre=?

                        GROUP BY  nom, trimestre ORDER BY asco, classe, trimestre""", param)

    res = cur.fetchall()
    c = 0
    n = 0

    for row in res:
        c += row[3]
        n += 1

    moy = c / n

    cd = 0
    for row in res:
        if row[3] > moy:
            cd += 1
    con.commit()
    con.close()
    return cd


""" 15- Fonction des bulletins annuels _____________________"""


def bull_ann():
    asco = show_asco_encours()
    param = (asco, asco)
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT asco, classe,

                    (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,

                    nom,

                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                    sum((coeff*note)) AS nc, sum(coeff) as coef,  

                    (sum(coeff*note)/sum(coeff)) as moyenne 

                    FROM Notes WHERE asco=?

                    GROUP BY asco, nom ORDER BY classe, nom, moyenne DESC""", param)

    res = cur.fetchall()
    r_final = []

    for row in res:
        i = 0
        count = 0
        while i < len(res):
            if res[i][1] == row[1]:
                if res[i][7] > row[7]:
                    count += 1
                else:
                    count = count
            else:
                count = count
            i += 1

        rang = count + 1

        row = row + (rang,)
        r_final.append(row)

    con.commit()
    con.close()
    return r_final


def moygen_ann(classe):
    asco = show_asco_encours()
    param = (asco, asco, classe)
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT classe, avg(moyenne) as moygen

                        FROM (SELECT asco, classe, nom, sum((coeff*note)) AS nc, sum(coeff) as coef,  (sum(coeff*note)/sum(coeff))as moyenne 

                        FROM Notes where asco = ?

                        GROUP BY asco, nom  ORDER BY classe, nom, moyenne DESC)

                        WHERE asco=? AND classe=?

                        GROUP BY classe ORDER BY asco, classe""", param)

    res = cur.fetchone()
    con.commit()
    con.close()
    return f"{res[1]:.2f}"


def notemin_ann(classe):
    asco = show_asco_encours()
    param = (asco, asco, classe)
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT asco, classe,

                    (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,

                    nom,

                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                    sum((coeff*note)) AS nc, sum(coeff) as coef,  (sum(coeff*note)/sum(coeff))as moyenne 

                    FROM Notes WHERE asco=? AND classe=?

                    GROUP BY asco, nom  ORDER BY classe, moyenne, nom""", param)

    res = cur.fetchone()
    con.commit()
    con.close()
    return f"{res[7]:.2f}"


def notemax_ann(classe):
    asco = show_asco_encours()
    param = (asco, asco, classe)
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT asco, classe,

                    (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,

                    nom,

                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                    sum((coeff*note)) AS nc, sum(coeff) as coef,  (sum(coeff*note)/sum(coeff))as moyenne 

                    FROM Notes WHERE asco=? AND classe=?

                    GROUP BY asco, nom ORDER BY classe, moyenne DESC, nom""", param)

    res = cur.fetchone()
    con.commit()
    con.close()
    return f"{res[7]:.2f}"


def tr_ann(classe):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    param = (show_asco_encours(), show_asco_encours(), classe)
    cur.execute("""SELECT asco, classe,

                    (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,

                    nom,

                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                    sum((coeff*note)) AS nc, sum(coeff) as coef,  (sum(coeff*note)/sum(coeff))as moyenne 

                    FROM Notes WHERE asco=? AND classe=?

                    GROUP BY asco, nom ORDER BY classe, nom, moyenne DESC""", param)

    res = cur.fetchall()
    a = effectif_classe(classe)
    count = 0
    for row in res:
        if float(row[7]) >= 10.0:
            count += 1
        else:
            count = count
    resultat = f"{(float(count / a) * 100):.2f}%"
    con.commit()
    con.close()
    return resultat


def te_ann(classe):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    param = (show_asco_encours(), show_asco_encours(), classe)
    cur.execute("""SELECT asco, classe,

                    (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,

                    nom,

                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                    sum((coeff*note)) AS nc, sum(coeff) as coef,  (sum(coeff*note)/sum(coeff))as moyenne 

                    FROM Notes WHERE asco=? AND classe=?

                    GROUP BY asco, nom  ORDER BY classe, nom, moyenne DESC""", param)

    res = cur.fetchall()
    a = effectif_classe(classe)
    count = 0
    for row in res:
        if float(row[7]) < 10.0:
            count += 1
        else:
            count = count
    resultat = f"{(float(count / a) * 100):.2f}%"
    con.commit()
    con.close()
    return resultat


def nb_admis_ann(classe):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    param = (show_asco_encours(), show_asco_encours(), classe)
    cur.execute("""SELECT asco, classe,

                    (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,

                    nom,

                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                    sum((coeff*note)) AS nc, sum(coeff) as coef,  (sum(coeff*note)/sum(coeff)) as moyenne 

                    FROM Notes WHERE asco=? AND classe=?

                    GROUP BY asco, nom ORDER BY classe, nom, moyenne DESC""", param)

    res = cur.fetchall()
    count = 0
    for row in res:
        if float(row[7]) >= 10:
            count += 1
        else:
            count = count

    con.commit()
    con.close()
    return count


def detail_bull_ann(classe, nom):
    asco = show_asco_encours()
    param = (asco, asco, classe, nom)
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT asco, classe,

                    (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,

                    nom, matiere,

                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                    avg(note) AS nc, avg(coeff) as coef,  (avg(note)*avg(coeff))as total

                    FROM Notes WHERE asco =? AND classe=? AND nom=?

                    GROUP BY asco, nom, matiere  ORDER BY classe, nom, matiere, total DESC""", param)

    res = cur.fetchall()
    r_final = []
    apprec = ''

    for row in res:
        if float(row[6]) == 0:
            apprec = 'nul'
        elif float(row[6]) > 0 and float(row[6]) <= 5.99:
            apprec = 'très faible'

        elif float(row[6]) > 5.99 and float(row[6]) <= 7.99:
            apprec = 'faible'

        elif float(row[6]) > 7.99 and float(row[6]) <= 9.99:
            apprec = 'médiocre'

        elif float(row[6]) == 10:
            apprec = 'moyen'

        elif float(row[6]) > 10 and float(row[6]) <= 12.99:
            apprec = 'passable'

        elif float(row[6]) > 12.99 and float(row[6]) <= 14.99:
            apprec = 'assez bien'

        elif float(row[6]) > 14.99 and float(row[6]) <= 16.99:
            apprec = 'bien'

        elif float(row[6]) > 16.99 and float(row[6]) <= 19.99:
            apprec = 'très bien'

        else:
            apprec = 'parfait'

        row = row + (apprec,)
        r_final.append(row)

    con.commit()
    con.close()
    return r_final


def note_trim_nom_t1(nom, mat):
    asco = show_asco_encours()
    trimestre = 'trimestre 1'
    param = (asco, asco, trimestre, nom, mat)
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT asco, classe,

                    (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,

                    (SELECT trim_nom FROM trimestres WHERE trimestres.trim_seq = notes.sequence) as trimestre,

                    nom, matiere,

                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                    avg(note) AS nc, avg(coeff) as coef,  (avg(note)*avg(coeff))as total

                    FROM Notes WHERE asco =?  AND trimestre=? AND nom=? AND matiere =?

                    GROUP BY asco, nom, trimestre, matiere  ORDER BY trimestre, classe, nom, matiere, total DESC""",
                param)

    res = cur.fetchone()

    con.commit()
    con.close()
    return res[7]


def note_trim_nom_t2(nom, mat):
    asco = show_asco_encours()
    trimestre = 'trimestre 2'
    param = (asco, asco, trimestre, nom, mat)
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT asco, classe,

                    (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,

                    (SELECT trim_nom FROM trimestres WHERE trimestres.trim_seq = notes.sequence) as trimestre,

                    nom, matiere,

                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                    avg(note) AS nc, avg(coeff) as coef,  (avg(note)*avg(coeff))as total

                    FROM Notes WHERE asco =?  AND trimestre=? AND nom=? AND matiere =?

                    GROUP BY asco, nom, trimestre, matiere  ORDER BY trimestre, classe, nom, matiere, total DESC""",
                param)

    res = cur.fetchone()

    con.commit()
    con.close()
    return res[7]


def note_trim_nom_t3(nom, mat):
    asco = show_asco_encours()
    trimestre = 'trimestre 3'
    param = (asco, asco, trimestre, nom, mat)
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    cur.execute("""SELECT asco, classe,

                    (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,

                    (SELECT trim_nom FROM trimestres WHERE trimestres.trim_seq = notes.sequence) as trimestre,

                    nom, matiere,

                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                    avg(note) AS nc, avg(coeff) as coef,  (avg(note)*avg(coeff))as total

                    FROM Notes WHERE asco =?  AND trimestre=? AND nom=? AND matiere =?

                    GROUP BY asco, nom, trimestre, matiere  ORDER BY trimestre, classe, nom, matiere, total DESC""",
                param)

    res = cur.fetchone()

    con.commit()
    con.close()
    return res[7]


def rech_bull_trim1(nom):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    trimestre = 'trimestre 1'
    param = (show_asco_encours(), show_asco_encours(), nom, trimestre)
    cur.execute("""SELECT asco, classe,

                    (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,

                    (SELECT trim_nom FROM trimestres WHERE trimestres.trim_seq = notes.sequence) as trimestre,

                    nom,

                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                    sum((coeff*note)) AS nc, sum(coeff) as coef,  

                    (sum(coeff*note)/sum(coeff)) as moyenne 

                    FROM Notes WHERE asco=? AND nom =? AND trimestre =?

                    GROUP BY asco, nom, trimestre  ORDER BY classe, trimestre, nom, moyenne DESC""", param)

    res = cur.fetchone()
    con.commit()
    con.close()
    return res[8]


def rech_bull_trim2(nom):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    trimestre = 'trimestre 2'
    param = (show_asco_encours(), show_asco_encours(), nom, trimestre)
    cur.execute("""SELECT asco, classe,

                    (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,

                    (SELECT trim_nom FROM trimestres WHERE trimestres.trim_seq = notes.sequence) as trimestre,

                    nom,

                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                    sum((coeff*note)) AS nc, sum(coeff) as coef,  

                    (sum(coeff*note)/sum(coeff)) as moyenne 

                    FROM Notes WHERE asco=? AND nom =? AND trimestre =?

                    GROUP BY asco, nom, trimestre  ORDER BY classe, trimestre, nom, moyenne DESC""", param)

    res = cur.fetchone()
    con.commit()
    con.close()
    return res[8]


def rech_bull_trim3(nom):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    trimestre = 'trimestre 3'
    param = (show_asco_encours(), show_asco_encours(), nom, trimestre)
    cur.execute("""SELECT asco, classe,

                    (SELECT count(ins_eleve) FROM inscriptions WHERE ins_classe = Notes.classe) as effectif,

                    (SELECT trim_nom FROM trimestres WHERE trimestres.trim_seq = notes.sequence) as trimestre,

                    nom,

                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                    sum((coeff*note)) AS nc, sum(coeff) as coef,  

                    (sum(coeff*note)/sum(coeff)) as moyenne 

                    FROM Notes WHERE asco=? AND nom =? AND trimestre =?

                    GROUP BY asco, nom, trimestre  ORDER BY classe, trimestre, nom, moyenne DESC""", param)

    res = cur.fetchone()
    con.commit()
    con.close()
    return res[8]


def notes_groupe_ann(classe, nom):
    con = sqlite3.connect(my_base)
    cur = con.cursor()
    asco = show_asco_encours()
    param = (asco, asco, classe, nom)

    cur.execute("""SELECT asco, classe,

                    nom, matiere,

                    (SELECT groupe FROM matieres WHERE mat_niv = (SELECT niveau FROM Classes WHERE classe_nom = classe) AND matiere = notes.matiere) as groupe,

                    (SELECT professeur FROM prof_titus WHERE asco=? AND classe = Notes.classe) as titus,

                    avg(note) AS nc, avg(coeff) as coef,  (avg(note)*avg(coeff))as total

                    FROM Notes WHERE asco =?  AND classe =? AND nom=?

                    GROUP BY asco, nom, matiere  ORDER BY classe, nom, matiere, total DESC""", param)

    res = cur.fetchall()
    r_final = []

    for row in res:
        if float(row[6]) == 0:
            apprec = 'nul'
        elif 0 < float(row[6]) <= 5.99:
            apprec = 'très faible'

        elif 5.99 < float(row[6]) <= 7.99:
            apprec = 'faible'

        elif 7.99 < float(row[6]) <= 9.99:
            apprec = 'médiocre'

        elif float(row[6]) == 10:
            apprec = 'moyen'

        elif 10 < float(row[6]) <= 12.99:
            apprec = 'passable'

        elif 12.99 < float(row[6]) <= 14.99:
            apprec = 'assez bien'

        elif 14.99 < float(row[6]) <= 16.99:
            apprec = 'bien'

        elif 16.99 < float(row[6]) <= 19.99:
            apprec = 'très bien'

        else:
            apprec = 'parfait'

        new_row = row + (apprec,)
        r_final.append(new_row)

    con.commit()
    con.close()
    return r_final


""" Fin des Fonction des bulletins annuels _____________________"""

# pensions = global_pension()
#
#
#
# all_pensions = []
# for data in pensions:
#     dico = {
#         'asco': data[0], 'eleve': data[1], 'classe': data[2], 'versé': data[5], 'pension': data[4],
#         'reste': data[6], 'statut': data[7],
#     }
#     all_pensions.append(dico)
#
# for row in all_pensions:
#     print(row)
#
# my_pension = 0
# total = 0
# for row in all_pensions:
#     if row["eleve"] == "MINTYENE RITA":
#         my_pension += row['versé']
#         total += row['pension']
#
# print(my_pension, total)





