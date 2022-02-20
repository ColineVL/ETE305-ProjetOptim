from modelisation.readExcel import nbHeures


def ajouterObjectif(mesZones, problem):
    """Définition de l'objectif"""
    # On veut réduire le coût de l'électricité
    coutProduction = 0
    # Quand les usines s'allument, ça coute de l'argent
    for zone in mesZones.values():
        for prod in zone.producteursDispatchable:
            for h in range(nbHeures - 1):
                if (
                    prod.variablesProduction[h] == 0
                    and prod.variablesProduction[h + 1] == 1
                ):
                    coutProduction += prod.coutAllumage
    # Cout d'utilisation de carburant
    coutProduction += sum(
        zone.calculerCoutProductionZone() for zone in mesZones.values()
    )
    # Fonction objectif
    problem += coutProduction
