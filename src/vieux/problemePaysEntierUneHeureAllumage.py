import pulp

import vieux.consommation as consommation
from producteurs import tousProducteurs

""" Problème version 2 """
""" On ne considère pas l'interconnexion : on peut échanger tout ce qu'on veut entre le Sud et le Nord """
""" Ce problème ne se déroule que sur une seule heure, on a une seule donnée de consommation """
""" Cette fois on peut allumer et éteindre des unités d'un site de production """

# Pendant une certaine heure
# Chaque centrale a une certaine puissance
# La somme doit atteindre la demande
# On calcule le cout total -> à minimiser

# Pratique
nbProducteurs = len(tousProducteurs)

# La demande
demande = consommation.consoTotale

# On crée le problème de minimisation du coût
problem = pulp.LpProblem("PaysEntierAllumage", pulp.LpMinimize)

# Les producteurs : on crée des variables pour chacun d'entre eux
variablesProd = [
    pulp.LpVariable(prod.nomCentrale, 0, prod.puissanceMax) for prod in tousProducteurs
]

variablesOnOff = [
    pulp.LpVariable(f"on_{prod.nomCentrale}", cat=pulp.LpBinary)
    for prod in tousProducteurs
]

# On ajoute des contraintes
for i in range(nbProducteurs):
    problem += (
        variablesProd[i] >= tousProducteurs[i].puissanceMin * variablesOnOff[i]
    )  # if 'on' produce at least min
    problem += (
        variablesProd[i] <= tousProducteurs[i].puissanceMax * variablesOnOff[i]
    )  # if 'on' produce at most max, if 'off' produce 0

problem += sum(variablesProd) >= demande


# On définit l'objectif
problem += sum(
    variablesProd[i] * tousProducteurs[i].coutMarginal for i in range(nbProducteurs)
)

# On vérifie que pulp arrive à trouver une solution
assert pulp.LpStatus[problem.solve()] == "Optimal"

# On extrait la solution
solution = [pulp.value(var) for var in variablesProd]

# On affiche le résultat
for i in range(nbProducteurs):
    prod = tousProducteurs[i]
    remarque = ""
    if solution[i] == prod.puissanceMax:
        remarque = ">> MAXIMUM"
    if solution[i] == prod.puissanceMin:
        remarque = "-- Minimum"
    if solution[i] == 0.0:
        remarque = "...eteint"

    print(f"Centrale {prod.nomCentrale} : {solution[i]} {remarque}")

print(sum(solution))
