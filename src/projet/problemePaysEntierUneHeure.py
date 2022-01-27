import pulp

import consommation
from producteurs import tousProducteurs

""" On ne considère pas l'interconnexion : on peut échanger tout ce qu'on veut entre le Sud et le Nord """
""" Ce problème ne se déroule que sur une seule heure, on a une seule donnée de consommation """

# Pendant une certaine heure
# Chaque centrale a une certaine puissance
# La somme doit atteindre la demande
# On calcule le cout total -> à minimiser

# Pratique
nbProducteurs = len(tousProducteurs)

# La demande
demande = consommation.consoTotale

# On crée le problème de minimisation du coût
problem = pulp.LpProblem("PaysEntier", pulp.LpMinimize)

# Les producteurs : on crée des variables pour chacun d'entre eux
variables = [
    pulp.LpVariable(prod.nomCentrale, prod.puissanceMin, prod.puissanceMax)
    for prod in tousProducteurs
]

# On ajoute des contraintes
for i in range(nbProducteurs):
    problem += variables[i] >= tousProducteurs[i].puissanceMin
    problem += variables[i] <= tousProducteurs[i].puissanceMax

problem += sum(variables) >= demande


# On définit l'objectif
problem += sum(
    variables[i] * tousProducteurs[i].coutMarginal for i in range(nbProducteurs)
)

# On vérifie que pulp arrive à trouver une solution
assert pulp.LpStatus[problem.solve()] == "Optimal"

# On extrait la solution
solution = [pulp.value(var) for var in variables]

# On affiche le résultat
for i in range(nbProducteurs):
    prod = tousProducteurs[i]
    remarque = ""
    if solution[i] == prod.puissanceMax:
        remarque = ">> MAXIMUM"
    if solution[i] == prod.puissanceMin:
        remarque = "-- Minimum"

    print(f"Centrale {prod.nomCentrale} : {solution[i]} {remarque}")

print(sum(solution))
