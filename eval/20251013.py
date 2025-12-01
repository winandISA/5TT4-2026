import random

joueurs = {"Wall-e" : {"nom": "Joueur", "pv": 10, "energie": 0},
           "ED 209" : {"nom": "Ennemi", "pv": 10, "energie": 0}}

def printEtat():
    for k, v in joueurs.items():
        print(f"Le joueur {k} a {v["pv"]} points de vie et {v['energie']} energies")

def choix_joueur():
    while True:
        choix = input("""Choisis ton action pour ce tour
        1 - Attaquer
        2 - Defendre
        3 - Soigner
        4 - Charger energie
        5 - tirer projectile""")
        if choix.isdigit():
            return int(choix)

def choix_pc():
    if joueurs["ED 209"]["pv"] < 4:
        return 3
    elif joueurs["Wall-e"]["energie"] * 3 > joueurs["ED 209"]["pv"] :
        return 2
    elif joueurs["Wall-e"]["pv"] < 3:
        return 1
    elif joueurs["ED 209"]["energie"] * 3 > joueurs["Wall-e"]["pv"] + 3 :
        return 5
    else:
        return 4

def tourDeJeu(joueur, adversaire, choixJoueur, choixAdversaire):
    attaque = 0
    if choixJoueur == 3:
        joueur["pv"] += 4
        if joueur["pv"] > 10:
            joueur["pv"] = 10
    elif choixJoueur == 1:
        attaque = 2
    elif choixJoueur == 5:
        attaque = joueur["energie"] * 3
        joueur["energie"] = 0
    elif choixJoueur == 4:
        joueur["energie"] += 1
    if attaque > 0:
        adversaire["pv"] -= attaque if choixAdversaire != 2 else attaque // 2

def jeu():
    print("Début du jeu")

    while joueurs["Wall-e"]["pv"] > 0 and joueurs["ED 209"]["pv"] > 0:
        printEtat()
        choixJoueur = choix_joueur()
        choixPC = choix_pc()
        tourDeJeu(joueurs["Wall-e"], joueurs["ED 209"], choixJoueur, choixPC)
        tourDeJeu(joueurs["ED 209"], joueurs["Wall-e"], choixPC, choixJoueur)

    if joueurs["Wall-e"]["pv"] > 0 and joueurs["ED 209"]["pv"] > 0:
        print("match nul")
    elif joueurs["ED 209"]["pv"] > 0:
        print("victoire ED 209")
    else:
        print("victoire Wall-e")
jeu()