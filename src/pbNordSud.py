import pulp
import matplotlib.pyplot as plt

from readExcel import consoSud, consoNord, nbHeures
from producteurs import (
    producteursDispatchablesNord,
    producteursDispatchablesSud,
    producteursFatalNord,
    producteursFatalSud,
)
from interco import capaciteIntercoNordSud, capaciteIntercoSudNord

""" Problème version 4 """
""" Le Sud et le Nord ont des producteurs différents """
""" Il y a une interconnexion entre les deux, pour transférer de l'électricité """
""" Ce problème se déroule sur plusieurs heures, on a donc autant de données de consommation """
""" On peut allumer et éteindre des unités d'un site de production """

# La demande
assert len(consoSud) == len(consoNord) == nbHeures

# On crée le problème de minimisation du coût
problem = pulp.LpProblem("NordSudAnnee", pulp.LpMinimize)

# Les producteurs dispatchables : on crée des variables pour chacun d'entre eux
# On va obtenir une matrice :
# variablesProd[x][i][h] = producteur i à l'heure h, avec x = 0 pour Nord, x = 1 pour Sud
variablesProd = []
variablesProd.append(
    [
        [
            pulp.LpVariable(f"{prod.nomCentrale}_{h}", 0, prod.puissanceMax)
            for h in range(nbHeures)
        ]
        for prod in producteursDispatchablesNord
    ]
)
variablesProd.append(
    [
        [
            pulp.LpVariable(f"{prod.nomCentrale}_{h}", 0, prod.puissanceMax)
            for h in range(nbHeures)
        ]
        for prod in producteursDispatchablesSud
    ]
)

# On off : les usines peuvent s'éteindre. Même format
variablesOnOff = []
variablesOnOff.append(
    [
        [
            pulp.LpVariable(f"on_{prod.nomCentrale}_{h}", cat=pulp.LpBinary)
            for h in range(nbHeures)
        ]
        for prod in producteursDispatchablesNord
    ]
)
variablesOnOff.append(
    [
        [
            pulp.LpVariable(f"on_{prod.nomCentrale}_{h}", cat=pulp.LpBinary)
            for h in range(nbHeures)
        ]
        for prod in producteursDispatchablesSud
    ]
)

# Interconnexion : le Sud peut envoyer de l'électricité au Nord et inversement
# intercoNordSud[h] = le Nord envoie tant au Sud à l'heure h
intercoNordSud = [
    pulp.LpVariable(f"intercoNS_{h}", 0, capaciteIntercoNordSud)
    for h in range(nbHeures)
]
intercoSudNord = [
    pulp.LpVariable(f"intercoSN_{h}", 0, capaciteIntercoSudNord)
    for h in range(nbHeures)
]

# On ajoute des contraintes : puissance minimum, maximum
for h in range(nbHeures):
    zone = 0  # Nord
    for i in range(len(producteursDispatchablesNord)):
        problem += (
            variablesProd[zone][i][h]
            >= producteursDispatchablesNord[i].puissanceMin * variablesOnOff[zone][i][h]
        )  # if 'on' produce at least min
        problem += (
            variablesProd[zone][i][h]
            <= producteursDispatchablesNord[i].puissanceMax * variablesOnOff[zone][i][h]
        )  # if 'on' produce at most max, if 'off' produce 0
    zone = 1  # Sud
    for i in range(len(producteursDispatchablesSud)):
        problem += (
            variablesProd[zone][i][h]
            >= producteursDispatchablesSud[i].puissanceMin * variablesOnOff[zone][i][h]
        )  # if 'on' produce at least min
        problem += (
            variablesProd[zone][i][h]
            <= producteursDispatchablesSud[i].puissanceMax * variablesOnOff[zone][i][h]
        )  # if 'on' produce at most max, if 'off' produce 0

# Contrainte : il faut satisfaire la demande, à la fois au nord et au sud
# Au Nord : à chaque heure, prodNordDisp + prodNordFatal + intercoSN - intercoNS >= demandeNord
for h in range(nbHeures):
    problem += (
        sum([variablesProd[0][i][h] for i in range(len(producteursDispatchablesNord))])
        + sum(prod.production[h] for prod in producteursFatalNord)
        + intercoSudNord[h]
        - intercoNordSud[h]
        >= consoNord[h]
    )
    problem += (
        sum([variablesProd[1][i][h] for i in range(len(producteursDispatchablesSud))])
        + sum([prod.production[h] for prod in producteursFatalSud])
        - intercoSudNord[h]
        + intercoNordSud[h]
        >= consoSud[h]
    )

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
for h in range(nbHeures):
    for i in range(len(producteursDispatchablesNord)):
        somme += variablesProd[0][i][h] * producteursDispatchablesNord[i].coutMarginal
    for i in range(len(producteursDispatchablesSud)):
        somme += variablesProd[1][i][h] * producteursDispatchablesSud[i].coutMarginal
problem += somme

# On vérifie que pulp arrive à trouver une solution
assert pulp.LpStatus[problem.solve()] == "Optimal"

# On extrait la solution
# solutions[i] = évolution de la prod sur nbHeures du producteur i, array de nbHeures valeurs
solutionsNord = [
    [pulp.value(var[h]) for h in range(nbHeures)] for var in variablesProd[0]
]
solutionsSud = [
    [pulp.value(var[h]) for h in range(nbHeures)] for var in variablesProd[1]
]

# On affiche le résultat
# Au Nord
plt.figure("tous les producteurs dispatchables nord")
plt.plot(consoNord, "b", label="Demande Nord")

for i in range(len(producteursDispatchablesNord)):
    plt.plot(solutionsNord[i], label=producteursDispatchablesNord[i].nomCentrale)

plt.legend()

# Au Sud

# Comparer demande et prod
plt.figure("comparer demande et prod")
plt.plot(consoNord, "b", label="Demande Nord")
plt.plot(consoSud, "r", label="Demande Sud")
prodTotaleNord = [
    sum([solutionsNord[i][h] for i in range(len(producteursDispatchablesNord))])
    for h in range(nbHeures)
]
plt.plot(prodTotaleNord, label="Production totale Nord")
prodTotaleSud = [
    sum([solutionsSud[i][h] for i in range(len(producteursDispatchablesSud))])
    for h in range(nbHeures)
]
plt.plot(prodTotaleSud, label="Production totale Sud")
plt.legend()

plt.show()

print(f"Cout total : {pulp.value(problem.objective)}")
# Avec interco : 91256623.56612028
# Sans interco : 91256944.56756029
# -> 300€ de différence sur l'année, c'est rien
