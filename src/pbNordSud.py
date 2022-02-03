import pulp
import matplotlib.pyplot as plt

from consommation import consoJourneeNord, consoJourneeSud
from producteurs import producteursNord, producteursSud

""" Problème version 4 """
""" Le Sud et le Nord ont des producteurs différents """
""" Il y a une interconnexion entre les deux, pour transférer de l'électricité """
""" Ce problème se déroule sur plusieurs heures (disons 24), on a donc autant de données de consommation """
""" On peut allumer et éteindre des unités d'un site de production """

# Pratique
nbProducteursNord = len(producteursNord)
nbProducteursSud = len(producteursSud)


# La demande
demandeNord = consoJourneeNord
demandeSud = consoJourneeSud
nbHeures = len(demandeNord)
assert len(demandeNord) == len(demandeSud)

# On crée le problème de minimisation du coût
problem = pulp.LpProblem("NordSudJournee", pulp.LpMinimize)

# Les producteurs : on crée des variables pour chacun d'entre eux
# On va obtenir une matrice :
# variablesProd[x][i][h] = producteur i à l'heure h, avec x = 0 pour Nord, x = 1 pour Sud
variablesProd = []
variablesProd.append(
    [
        [
            pulp.LpVariable(f"{prod.nomCentrale}_{h}", 0, prod.puissanceMax)
            for h in range(nbHeures)
        ]
        for prod in producteursNord
    ]
)
variablesProd.append(
    [
        [
            pulp.LpVariable(f"{prod.nomCentrale}_{h}", 0, prod.puissanceMax)
            for h in range(nbHeures)
        ]
        for prod in producteursSud
    ]
)

variablesOnOff = []
variablesOnOff.append(
    [
        [
            pulp.LpVariable(f"on_{prod.nomCentrale}_{h}", cat=pulp.LpBinary)
            for h in range(nbHeures)
        ]
        for prod in producteursNord
    ]
)
variablesOnOff.append(
    [
        [
            pulp.LpVariable(f"on_{prod.nomCentrale}_{h}", cat=pulp.LpBinary)
            for h in range(nbHeures)
        ]
        for prod in producteursSud
    ]
)

# On ajoute des contraintes : puissance minimum, maximum
for h in range(nbHeures):
    zone = 0
    for i in range(nbProducteursNord):
        problem += (
            variablesProd[zone][i][h]
            >= producteursNord[i].puissanceMin * variablesOnOff[zone][i][h]
        )  # if 'on' produce at least min
        problem += (
            variablesProd[zone][i][h]
            <= producteursNord[i].puissanceMax * variablesOnOff[zone][i][h]
        )  # if 'on' produce at most max, if 'off' produce 0
    zone = 1
    for i in range(nbProducteursSud):
        problem += (
            variablesProd[zone][i][h]
            >= producteursNord[i].puissanceMin * variablesOnOff[zone][i][h]
        )  # if 'on' produce at least min
        problem += (
            variablesProd[zone][i][h]
            <= producteursNord[i].puissanceMax * variablesOnOff[zone][i][h]
        )  # if 'on' produce at most max, if 'off' produce 0

# Contrainte : il faut satisfaire la demande, à la fois au nord et au sud
for h in range(nbHeures):
    problem += (
        sum([variablesProd[0][i][h] for i in range(nbProducteursNord)])
        >= demandeNord[h]
    )
    problem += (
        sum([variablesProd[1][i][h] for i in range(nbProducteursSud)]) >= demandeSud[h]
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
    for i in range(nbProducteursNord):
        somme += variablesProd[0][i][h] * producteursNord[i].coutMarginal
    for i in range(nbProducteursSud):
        somme += variablesProd[1][i][h] * producteursSud[i].coutMarginal
problem += somme

# On vérifie que pulp arrive à trouver une solution
print(pulp.LpStatus[problem.solve()])
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
plt.figure("tous les producteurs nord")
plt.plot(demandeNord, "b", label="Demande Nord")

for i in range(nbProducteursNord):
    plt.plot(solutionsNord[i], label=producteursNord[i].nomCentrale)

plt.legend()

# Au Sud
plt.figure("tous les producteurs sud")
plt.plot(demandeSud, "b", label="Demande Sud")

for i in range(nbProducteursSud):
    plt.plot(solutionsSud[i], label=producteursSud[i].nomCentrale)

plt.legend()

# Comparer demande et prod
plt.figure("comparer demande et prod")
plt.plot(demandeNord, "b", label="Demande Nord")
plt.plot(demandeSud, "r", label="Demande Sud")
prodTotaleNord = [
    sum([solutionsNord[i][h] for i in range(nbProducteursNord)])
    for h in range(nbHeures)
]
plt.plot(prodTotaleNord, label="Production totale Nord")
prodTotaleSud = [
    sum([solutionsSud[i][h] for i in range(nbProducteursSud)]) for h in range(nbHeures)
]
plt.plot(prodTotaleSud, label="Production totale Sud")
plt.legend()

plt.show()
