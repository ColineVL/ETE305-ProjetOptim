import pulp

from modelisation.readExcel import nbHeures, capaciteIntercoInitiale
import modelisation.ourValues as ourValues


def ajoutVariables(mesZones):
    """Création des variables de production"""

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
