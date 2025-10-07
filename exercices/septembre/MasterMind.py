import random

couleursDispo = ["R", "V", "N", "J", "O", "B"]
def analyseReponse(proposition):
    reponse = {"R":0, "V":0, "N":0, "J":0, "O":0, "B":0, "autre": 0}
    if len(proposition) == 5:
        for element in proposition:
            if element in couleursDispo:
                reponse[element] += 1
            else:
                reponse["autre"] += 1
    else:
        reponse["autre"] += 1
    print(reponse)
    return reponse

listeATrouver = []
for i in range(5):
    listeATrouver.append(random.choice(couleursDispo))

trouve = 0
i = 0
while trouve != 5 and i < 10:
    print(listeATrouver)
    proposition = input("""Entrez une proposition au format X X X X X
    Valeurs acceptée: Rouge R, Vert V, Noir N, Jaune J, Orange O, Bleu B """).upper().split(" ")
    returnValue = analyseReponse(proposition)
    if returnValue["autre"] == 0 :
        resultat = [" ", " ", " ", " ", " "]
        trouve = 0
        for j in range(len(proposition)):
            if proposition[j] == listeATrouver[j]:
                resultat[j] = "☑ "
                returnValue[proposition[j]] -= 1
                trouve += 1
            else:
                resultat[j] = "O "
        for j in range(len(proposition)):
            if proposition[j] != listeATrouver[j] and returnValue[proposition[j]] != 0:
                for i in range(len(proposition)):
                    if proposition[i] == listeATrouver[j] and proposition[i] != listeATrouver[i]:
                        resultat[j] = "✔ "
                        returnValue[proposition[j]] -= 1

        print(resultat)
        i +=1
    else:
        print("valeur incorrecte")
if trouve == 5:
    print("Gagné")
else:
    print("perdu")
print(listeATrouver)