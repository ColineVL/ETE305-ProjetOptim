import pulp
from postTraitementFiles.display import affichageResultats
from postTraitementFiles import writeExcel


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

    # On note les solutions dans un fichier excel
    writeExcel.writeResultsInExcel(mesZones, nbHeures)

    print(f"Cout total : {pulp.value(problem.objective)}")

    # Affichage de l'interco max
    for zone in mesZones.values():
        print(
            f"Interco vers {zone.nom.name} : { pulp.value(zone.capaciteIntercoVersMoi)}"
        )
        for prod in zone.producteursFatal:
            if prod.amelioration:
                print(f"Amelioration {prod.nomCentrale} : {pulp.value(prod.capacite)}")

    # Quelques plots
    affichageResultats(mesZones, nbHeures)
