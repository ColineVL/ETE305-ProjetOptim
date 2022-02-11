import matplotlib.pyplot as plt


def affichageResultats(mesZones, nbHeures):
    # # On affiche le résultat, dans chaque zone les productions de chaque producteur
    # for zone in mesZones.values():
    #     plt.figure(f"Tous les producteurs dispatchables {zone.nom}")
    #     plt.plot(zone.conso, "b", label=f"Demande {zone.nom}")
    #     for prod in zone.producteursDispatchable:
    #         plt.plot(prod.solutionProduction, label=prod.nomCentrale)
    #     plt.legend()
         
    for zone in mesZones.values():
        plt.figure(f"Tous les producteurs dispatchables {zone.nom}")

        # Demande
        plt.plot(zone.conso, "b", label=f"Demande {zone.nom}")

        # # Energie renouvelable
        # RenewSum = [0.]
        # for h in range(nbHeures):
        #     RenewSum.append(sum(prod.production[h] for prod in zone.producteursFatal))
        # plt.plot(zone.productionFatal)


        # Producteur Dispatchable + Interconnexion
        ProdSum = [0.] * nbHeures
        for prod in zone.producteursDispatchable:
            for h in range(nbHeures):
                ProdSum[h] += prod.solutionProduction[h] + zone.solutionIntercoVersMoi[h] - mesZones["Sud" if zone.nom == "Nord" else "Nord"].solutionIntercoVersMoi[h] +zone.productionFatal[h]
            plt.plot(ProdSum,label=prod.nomCentrale)
            # plt.fill(TotalSum,label=prod.nomCentrale)
            # plt.fill_between(ProdSum,interpolate=True)
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
