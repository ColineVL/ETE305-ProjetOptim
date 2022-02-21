import pulp

from postTraitementFiles.display import affichageResultats
from postTraitementFiles.extractionSolutions import extraireSolutions
from postTraitementFiles.writeExcel import writeResultsInExcel


def traitementResultats(problem, mesZones, nbHeures):

    # On extrait la solution du problème, on la range dans nos producteurs
    extraireSolutions(mesZones, nbHeures)

    # On note les solutions dans un fichier excel
    writeResultsInExcel(mesZones, nbHeures)

    print(f"Cout total : {pulp.value(problem.objective)}\n")

    # Affichage de l'interco max
    for zone in mesZones.values():
        print(f"Interco vers {zone.nom.name} : { zone.solutionCapaciteIntercoVersMoi}")
    print("\n")

    # Affichage des constructions de fatal
    for zone in mesZones.values():
        for prod in zone.producteursFatal:
            if prod.amelioration:
                print(
                    f"Amelioration {prod.nomCentrale} : {prod.amelioration.solutionCapacite}"
                )
    print("\n")

    # Affichage des constructions de dispatchable
    for zone in mesZones.values():
        for prod in zone.producteursDispatchable:
            if prod.amelioration:
                print(
                    f"Amelioration {prod.nomCentrale} : {prod.amelioration.solutionCentraleConstruite}"
                )

    # Quelques plots
    affichageResultats(mesZones, nbHeures)
