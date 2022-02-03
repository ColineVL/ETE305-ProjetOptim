import pulp
import matplotlib.pyplot as plt

import vieux.consommation as consommation
from producteurs import tousProducteurs

""" Problème version 3 """
""" On ne considère pas l'interconnexion : on peut échanger tout ce qu'on veut entre le Sud et le Nord """
""" Ce problème se déroule sur plusieurs heures (disons 24), on a donc autant de données de consommation """
""" On peut allumer et éteindre des unités d'un site de production, et il faut respecter des durées minimales d'allumage """

# Pratique
nbProducteurs = len(tousProducteurs)

# La demande
demande = consommation.consoJournee
nbHeures = len(demande)

# On crée le problème de minimisation du coût
problem = pulp.LpProblem("PaysEntierAllumageJournee", pulp.LpMinimize)

# Les producteurs : on crée des variables pour chacun d'entre eux
# On va obtenir une matrice :
# variablesProd[i][h] = producteur i à l'heure h
variablesProd = [
    [
        pulp.LpVariable(f"{prod.nomCentrale}_{h}", 0, prod.puissanceMax)
        for h in range(nbHeures)
    ]
    for prod in tousProducteurs
]

variablesOnOff = [
    [
        pulp.LpVariable(f"on_{prod.nomCentrale}_{h}", cat=pulp.LpBinary)
        for h in range(nbHeures)
    ]
    for prod in tousProducteurs
]

# On ajoute des contraintes : puissance minimum, maximum
for i in range(nbProducteurs):
    for h in range(nbHeures):
        problem += (
            variablesProd[i][h]
            >= tousProducteurs[i].puissanceMin * variablesOnOff[i][h]
        )  # if 'on' produce at least min
        problem += (
            variablesProd[i][h]
            <= tousProducteurs[i].puissanceMax * variablesOnOff[i][h]
        )  # if 'on' produce at most max, if 'off' produce 0

# Contrainte : il faut satisfaire la demande
for h in range(nbHeures):
    problem += sum([variablesProd[i][h] for i in range(nbProducteurs)]) >= demande[h]

# Contrainte : si on allume, il faut rester allumé un certain temps
# for i in range(nbProducteurs):
#     dureeMin = tousProducteurs[i].dureeMinAllumage
#     if dureeMin > 1:
#         for h in range(1, nbHeures - (dureeMin - 2)):
#             # Pour dureeMin = 6:
#             # A h, si h-1 est allumé, on fait ce qu'on veut
#             # Si h-1 est éteint et que parmi h+1, h+2, h+3 ou h+4 à un moment on est éteint,
#             # alors il faut être éteint à h
#             # En gros si à h-1 on est à 0 et que une fois dans h+1, h+2, h+3 ou h+4 on est à 0, alors il faut être à 0
#             # Donc [h-1] <= 4 + [h-1] - [h+1] - [h+2] - [h+3] - [h+4]
#             somme = sum([variablesOnOff[i][h + x] for x in range(1, (dureeMin - 1))])
#             problem += variablesOnOff[i][h] <= variablesOnOff[i][h - 1] + 4 - somme


# On définit l'objectif
somme = 0
for i in range(nbProducteurs):
    for h in range(nbHeures):
        somme += variablesProd[i][h] * tousProducteurs[i].coutMarginal

problem += somme

# On vérifie que pulp arrive à trouver une solution
assert pulp.LpStatus[problem.solve()] == "Optimal"

# On extrait la solution
# solutions[i] = évolution de la prod sur nbHeures du producteur i, array de nbHeures valeurs
solutions = [[pulp.value(var[h]) for h in range(nbHeures)] for var in variablesProd]

# On affiche le résultat
plt.figure("tous les producteurs")
plt.plot(demande, "b", label="Demande")

for i in range(nbProducteurs):
    plt.plot(solutions[i], label=tousProducteurs[i].nomCentrale)

plt.legend()

plt.figure("comparer demande et prod")
plt.plot(demande, "b", label="Demande")
prodTotale = [
    sum([solutions[i][h] for i in range(nbProducteurs)]) for h in range(nbHeures)
]
plt.plot(prodTotale, label="Production totale")
plt.legend()

plt.show()
