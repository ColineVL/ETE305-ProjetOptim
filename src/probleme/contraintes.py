from modelisation.readExcel import nbHeures, capaciteIntercoInitiale
import modelisation.ourValues as ourValues


def satisfactionDemande(mesZones, problem):
    for zone in mesZones.values():
        for h in range(nbHeures):
            # Les producteurs fatal sont augmentés en fonction de leur amélioration
            for prod in zone.producteursFatal:
                if prod.amelioration:
                    prod.production[h] = prod.production[h] * (
                        prod.capacite * (1 / prod.amelioration.capaciteInitiale)
                    )

            problem += (
                sum(
                    prod.variablesProduction[h] for prod in zone.producteursDispatchable
                )
                + sum(prod.production[h] for prod in zone.producteursFatal)
                + zone.intercoVersMoi[h]
                - mesZones[zone.autreZone()].intercoVersMoi[h]
                + ourValues.effacement
                >= zone.conso[h]
            )


def respectDuBudget(mesZones, problem):
    depenses = 0
    # On a augmenté l'interco
    depenses += sum(
        (zone.capaciteIntercoVersMoi - capaciteIntercoInitiale)
        * ourValues.coutAugmentationInterco
        for zone in mesZones.values()
    )

    # On a amélioré les fatal
    for zone in mesZones.values():
        for prod in zone.producteursFatal:
            if prod.amelioration:
                depenses += (
                    prod.capacite - prod.amelioration.capaciteInitiale
                ) * prod.amelioration.coutInvestissement

    problem += depenses <= ourValues.budgetTotal


def ajoutContraintes(mesZones, problem):
    """Ajout de contraintes"""

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

            # Contrainte d'interconnexion maximale : la capacité d'interconnexion effective doit être réaliste
            problem += zone.intercoVersMoi[h] <= zone.capaciteIntercoVersMoi

            # Contrainte de coût, on allume dans l'ordre :
            # Pour pouvoir allumer les TAC, il faut que tous les diesels soient on
            # Pour pouvoir allumer les diesels, il faut que tous les charbons soient on
            for prod in zone.producteursDispatchable:
                if prod.donnerMeilleursTypes():
                    # Il faut que toutes les usines moins chères soient on
                    producteursMieux = [
                        prod2
                        for prod2 in zone.producteursDispatchable
                        if prod2.type in prod.donnerMeilleursTypes()
                    ]
                    problem += len(producteursMieux) * prod.variablesOnOff[h] <= sum(
                        prod3.variablesOnOff[h] for prod3 in producteursMieux
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

    # Contrainte de satisfaction de la demande
    satisfactionDemande(mesZones, problem)

    """ Contrainte : respect du budget """
    respectDuBudget(mesZones, problem)
