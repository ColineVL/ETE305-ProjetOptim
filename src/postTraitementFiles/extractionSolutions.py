import pulp


def extraireSolutions(mesZones, nbHeures):
    """Extraire les solutions de pulp et les ranger dans nos modèles"""

    for zone in mesZones.values():
        # zone.solutionIntercoVersMoi from intercoVersMoi
        zone.solutionIntercoVersMoi = [
            pulp.value(zone.intercoVersMoi[h]) for h in range(nbHeures)
        ]
        # zone.solutionCapaciteIntercoVersMoi from capaciteIntercoVersMoi
        zone.solutionCapaciteIntercoVersMoi = pulp.value(zone.capaciteIntercoVersMoi)

        for prodDisp in zone.producteursDispatchable:
            # prodDispatchable.solutionProduction from variablesProduction
            prodDisp.solutionProduction = [
                pulp.value(prodDisp.variablesProduction[h]) for h in range(nbHeures)
            ]
            if prodDisp.amelioration:
                # prodDispatchable.solutionCentraleConstruite from centraleConstruite
                prodDisp.amelioration.solutionCentraleConstruite = pulp.value(
                    prodDisp.amelioration.centraleConstruite
                )

        for prodFatal in zone.producteursFatal:
            if prodFatal.amelioration:
                # prodFatal.solutionCapacite from capacite
                prodFatal.amelioration.solutionCapacite = pulp.value(
                    prodFatal.amelioration.capacite
                )
                print(prodFatal.amelioration.solutionCapacite)
