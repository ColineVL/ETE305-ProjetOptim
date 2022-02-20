import matplotlib.pyplot as plt
from modelisation.enums import TypeEnergie


def affichageResultats(mesZones, nbHeures):
    # On affiche le résultat, dans chaque zone les productions de chaque producteur

    for zone in mesZones.values():
        # Energie renouvelable
        # on a deja zone.productionFatal

        # Interco
        IntercoZone = [
            zone.solutionIntercoVersMoi[h]
            - mesZones[zone.autreZone()].solutionIntercoVersMoi[h]
            for h in range(nbHeures)
        ]

        # Charbon
        charbon = [
            sum(
                prod.solutionProduction[h]
                for prod in zone.producteursDispatchable
                if prod.type == TypeEnergie.CHARBON
            )
            for h in range(nbHeures)
        ]

        # Diesel
        diesel = [
            sum(
                prod.solutionProduction[h]
                for prod in zone.producteursDispatchable
                if prod.type == TypeEnergie.DIESEL
            )
            for h in range(nbHeures)
        ]

        # TAC
        tac = [
            sum(
                prod.solutionProduction[h]
                for prod in zone.producteursDispatchable
                if prod.type == TypeEnergie.TAC
            )
            for h in range(nbHeures)
        ]

        ## Plot
        plt.figure(f"Tous les producteurs dispatchables {zone.nom.name}")

        # Demande
        plt.plot(zone.conso, "b", label=f"Demande {zone.nom.name}")

        # Interco
        plt.fill_between(
            range(nbHeures), 0, IntercoZone, color="cyan", label=f"Interconnexion"
        )

        # Production Fatal
        Niveau1 = [IntercoZone[h] + zone.productionFatal[h] for h in range(nbHeures)]
        plt.fill_between(
            range(nbHeures),
            IntercoZone,
            Niveau1,
            color="red",
            label=f"Production Fatal",
        )

        # TAC
        Niveau2 = [
            IntercoZone[h] + zone.productionFatal[h] + tac[h] for h in range(nbHeures)
        ]
        plt.fill_between(range(nbHeures), Niveau1, Niveau2, color="green", label=f"TAC")

        # Diesel
        Niveau3 = [
            IntercoZone[h] + zone.productionFatal[h] + tac[h] + diesel[h]
            for h in range(nbHeures)
        ]
        plt.fill_between(
            range(nbHeures), Niveau2, Niveau3, color="yellow", label=f"Diesel"
        )

        # Charbon
        Niveau4 = [
            IntercoZone[h] + zone.productionFatal[h] + tac[h] + diesel[h] + charbon[h]
            for h in range(nbHeures)
        ]
        plt.fill_between(
            range(nbHeures), Niveau3, Niveau4, color="orange", label=f"Charbon"
        )
        # plt.fill_between(range(nbHeures),-0.01,0.01,color = 'white')
        plt.axhline(linewidth=1, color="black", linestyle="--")
        plt.legend()

        # On compare la demande et la production, sur les deux zones en même temps
    plt.figure("Comparer demande et production")
    for zone in mesZones.values():
        plt.plot(zone.conso, label=f"Demande {zone.nom.name}")
        prodTotale = [
            sum(prod.solutionProduction[h] for prod in zone.producteursDispatchable)
            for h in range(nbHeures)
        ]
        plt.plot(prodTotale, label=f"Production totale {zone.nom.name}")
        plt.legend()

    plt.show()
