import pulp

from postTraitementFiles.postTraitement import traitementResultats
from readExcel import nbHeures, capaciteIntercoInitiale
from modelisation.zones import mesZones, ZoneName
import modelisation.ourValues as ourValues

""" Problème version 4 """
""" Le Sud et le Nord ont des producteurs différents """
""" Il y a une interconnexion entre les deux, pour transférer de l'électricité """
""" Ce problème se déroule sur plusieurs heures, on a donc autant de données de consommation """
""" On peut allumer et éteindre des unités d'un site de production """


def main():
    # La demande
    assert (
        len(mesZones[ZoneName.SUD].conso)
        == len(mesZones[ZoneName.NORD].conso)
        == nbHeures
    )
    # On augmente un peu les consos
    for zone in mesZones.values():
        zone.conso = zone.conso * ourValues.facteurAugmentationConso

    # On crée le problème de minimisation du coût
    problem = pulp.LpProblem("NordSudAnnee", pulp.LpMinimize)

    """ Création des variables de production """

    for zone in mesZones.values():

        # Les producteurs dispatchables : on crée des variables pour chacun d'entre eux
        for prod in zone.producteursDispatchable:

            # Chaque producteur a son tableau de variables :
            # producteur.variablesProduction[h] = sa production à l'heure h
            prod.variablesProduction = [
                pulp.LpVariable(
                    f"{prod.nomCentrale}_{zone.nom.name}_{h}", 0, prod.puissanceMax
                )
                for h in range(nbHeures)
            ]

            # On crée aussi des variables OnOff :
            # producteur.variablesOnOff[h] = est-il allumé à l'heure h ?
            prod.variablesOnOff = [
                pulp.LpVariable(
                    f"on_{prod.nomCentrale}_{zone.nom.name}_{h}", cat=pulp.LpBinary
                )
                for h in range(nbHeures)
            ]

        # Interconnexion : le Sud peut envoyer de l'électricité au Nord et inversement
        # D'abord on crée une variable pour une borne max
        zone.capaciteIntercoVersMoi = pulp.LpVariable(
            f"max_interco_vers_{zone.nom.name}",
            capaciteIntercoInitiale,
            ourValues.capaciteIntercoMax,
        )
        # Ensuite on crée les valeurs d'interco heure par heure
        zone.intercoVersMoi = [
            pulp.LpVariable(
                f"interco_vers_{zone.nom.name}_{h}", 0, ourValues.capaciteIntercoMax
            )
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

            # Contrainte d'interconnexion maximale : la capacité d'interconnexion effective doit être réaliste
            problem += zone.intercoVersMoi[h] <= zone.capaciteIntercoVersMoi

            # Contrainte de satisfaction de la demande
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

    """ Contrainte : respect du budget """
    # On a augmenté l'interco
    problem += (
        sum(
            (zone.capaciteIntercoVersMoi - capaciteIntercoInitiale)
            * ourValues.coutAugmentationInterco
            for zone in mesZones.values()
        )
        <= ourValues.budgetTotal
    )

    """ Définition de l'objectif """
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

    """ Résolution du problème """

    # On vérifie que pulp arrive à trouver une solution
    assert pulp.LpStatus[problem.solve()] == "Optimal"

    """ Post-traitement """
    traitementResultats(problem, mesZones, nbHeures)


if __name__ == "__main__":
    main()
