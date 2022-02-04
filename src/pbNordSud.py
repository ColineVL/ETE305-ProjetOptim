import pulp
import matplotlib.pyplot as plt

from readExcel import nbHeures, effacement
from zone import mesZones

""" Problème version 4 """
""" Le Sud et le Nord ont des producteurs différents """
""" Il y a une interconnexion entre les deux, pour transférer de l'électricité """
""" Ce problème se déroule sur plusieurs heures, on a donc autant de données de consommation """
""" On peut allumer et éteindre des unités d'un site de production """

# La demande
assert len(mesZones["sud"].conso) == len(mesZones["nord"].conso) == nbHeures

# On crée le problème de minimisation du coût
problem = pulp.LpProblem("NordSudAnnee", pulp.LpMinimize)


""" Création des variables de production """

for zone in mesZones.values():

    # Les producteurs dispatchables : on crée des variables pour chacun d'entre eux
    for prod in zone.producteursDispatchable:

        # Chaque producteur a son tableau de variables :
        # producteur.variablesProduction[h] = sa production à l'heure h
        prod.variablesProduction = [
            pulp.LpVariable(f"{prod.nomCentrale}_{zone.nom}_{h}", 0, prod.puissanceMax)
            for h in range(nbHeures)
        ]

        # On crée aussi des variables OnOff :
        # producteur.variablesOnOff[h] = est-il allumé à l'heure h ?
        prod.variablesOnOff = [
            pulp.LpVariable(f"on_{prod.nomCentrale}_{zone.nom}_{h}", cat=pulp.LpBinary)
            for h in range(nbHeures)
        ]

    # Interconnexion : le Sud peut envoyer de l'électricité au Nord et inversement
    zone.intercoVersMoi = [
        pulp.LpVariable(f"interco_vers_{zone.nom}_{h}", 0, zone.capaciteIntercoVersMoi)
        for h in range(nbHeures)
    ]

""" Ajout de contraintes """

for zone in mesZones.values():
    for h in range(nbHeures):

        # Contrainte de puissance minimum, maximum
        for prod in zone.producteursDispatchable:
            problem += (
                prod.variablesProduction[h]
                >= prod.puissanceMin * prod.variablesOnOff[h]
            )  # if 'on' produce at least min
            problem += (
                prod.variablesProduction[h]
                <= prod.puissanceMax * prod.variablesOnOff[h]
            )  # if 'on' produce at most max, if 'off' produce 0

        # Contrainte de satisfaction de la demande
        problem += (
            sum(prod.variablesProduction[h] for prod in zone.producteursDispatchable)
            + sum(prod.production[h] for prod in zone.producteursFatal)
            + zone.intercoVersMoi[h]
            - mesZones["sud" if zone.nom == "Nord" else "nord"].intercoVersMoi[h]
            + effacement
            >= zone.conso[h]
        )

    # Contrainte d'allumage : il faut rester allumé un certain temps minimum
    for prod in zone.producteursDispatchable:
        minsteps = prod.dureeMinAllumage
        if minsteps > 1:
            for h in range(1, nbHeures):
                min_effectif = min(minsteps, nbHeures - h)
                problem += (
                    prod.variablesOnOff[h] - prod.variablesOnOff[h - 1]
                ) * min_effectif <= sum(
                    prod.variablesOnOff[t] for t in range(h, h + min_effectif)
                )

""" Définition de l'objectif """

# On veut réduire le coût de l'électricité
problem += sum(zone.calculerCoutProductionZone() for zone in mesZones.values())

""" Résolution du problème """

# On vérifie que pulp arrive à trouver une solution
assert pulp.LpStatus[problem.solve()] == "Optimal"

""" Post-traitement """

# On extrait la solution du problème, on la range dans nos producteurs
for zone in mesZones.values():
    for prod in zone.producteursDispatchable:
        prod.solutionProduction = [
            pulp.value(prod.variablesProduction[h]) for h in range(nbHeures)
        ]

# On affiche le résultat, dans chaque zone les productions de chaque producteur
for zone in mesZones.values():
    plt.figure(f"Tous les producteurs dispatchables {zone.nom}")
    plt.plot(zone.conso, "b", label=f"Demande {zone.nom}")
    for prod in zone.producteursDispatchable:
        plt.plot(prod.solutionProduction, label=prod.nomCentrale)
    plt.legend()

# On compare la demande et la production, sur les deux zones en même temps
plt.figure("Comparer demande et production")
for zone in mesZones.values():
    plt.plot(zone.conso, label=f"Demande {zone.nom}")
    prodTotale = [
        sum(prod.solutionProduction[h] for prod in zone.producteursDispatchable)
        for h in range(nbHeures)
    ]
    plt.plot(prodTotale, label=f"Production totale {zone.nom}")
    plt.legend()

plt.show()

print(f"Cout total : {pulp.value(problem.objective)}")
# Sur 100h interco : 10627214.780000005
# Sur l'année :      89424079.8299998
