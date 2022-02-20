import pulp
from postTraitementFiles.display import affichageResultats


def traitementResultats(problem, mesZones, nbHeures):

    # On extrait la solution du problème, on la range dans nos producteurs
    for zone in mesZones.values():
        for prod in zone.producteursDispatchable:
            prod.solutionProduction = [
                pulp.value(prod.variablesProduction[h]) for h in range(nbHeures)
            ]
        zone.solutionIntercoVersMoi = [
            pulp.value(zone.intercoVersMoi[h]) for h in range(nbHeures)
        ]

    print(f"Cout total : {pulp.value(problem.objective)}")

    # Affichage de l'interco max
    for zone in mesZones.values():
        print(
            f"Interco vers {zone.nom.name} : { pulp.value(zone.capaciteIntercoVersMoi)}"
        )

    # Quelques plots
    affichageResultats(mesZones, nbHeures)
