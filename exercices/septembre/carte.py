import random

cartes = ["As", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Valet", "Dame", "Roi"]
game = cartes.copy()
carteDeBase = random.choice(game)
game.remove(carteDeBase)
fini = False
while not fini:
    choix = input(f"La carte est {carteDeBase}, la suivante sera + ou -? ")
    carteAComparer = random.choice(game)
    game.remove(carteAComparer)
    print(f"la carte tirée est {carteAComparer}")
    if (choix == "+" and carteAComparer > carteDeBase) or (choix == "-" and carteAComparer < carteDeBase):
        if cartes.index(carteDeBase) > cartes.index(carteAComparer):
            print("perdu")
            fini = True
    carteDeBase = carteAComparer
    if len(game) == 0:
        print("gagné")
        fini = True