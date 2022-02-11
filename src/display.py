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
        # Energie renouvelable
        # on a deja zone.productionFatal

        # Interco
        IntercoZone = [
            zone.solutionIntercoVersMoi[h] - mesZones["Sud" if zone.nom == "Nord" else "Nord"].solutionIntercoVersMoi[h]
            for h in range(nbHeures)
        ]
        
        # Charbon
        charbon = [
            sum(
                prod.solutionProduction[h]
                for prod in zone.producteursDispatchable
                if prod.type == 'charbon'
            )
            for h in range(nbHeures)
        ]
        
        # Diesel
        diesel = [
            sum(
                prod.solutionProduction[h]
                for prod in zone.producteursDispatchable
                if prod.type == 'diesel'
            )
            for h in range(nbHeures)
        ]
    
        # TAC
        tac = [
            sum(
                prod.solutionProduction[h]
                for prod in zone.producteursDispatchable
                if prod.type == 'tac'
            )
            for h in range(nbHeures)
        ]
       


        # # Producteur Dispatchable + Interconnexion
        # ProdSum = [0.] * nbHeures
        # SolutionInterco = [0.] * nbHeures
        # for prod in zone.producteursDispatchable:
        #     for h in range(nbHeures):
        #         SolutionInterco[h] =  zone.solutionIntercoVersMoi[h] - mesZones["Sud" if zone.nom == "Nord" else "Nord"].solutionIntercoVersMoi[h]
        #         ProdSum[h] += prod.solutionProduction[h] + SolutionInterco[h] +zone.productionFatal[h]
        #     plt.plot(ProdSum,label=prod.nomCentrale)
        #     # plt.fill(TotalSum,label=prod.nomCentrale)
        #     # plt.fill_between(ProdSum,interpolate=True)
        # plt.legend()


    # # On compare la demande et la production, sur les deux zones en même temps
    # plt.figure("Comparer demande et production")
    # for zone in mesZones.values():
    #     plt.plot(zone.conso, label=f"Demande {zone.nom}")
    #     prodTotale = [
    #         sum(prod.solutionProduction[h] for prod in zone.producteursDispatchable)
    #         for h in range(nbHeures)
    #     ]
    #     plt.plot(prodTotale, label=f"Production totale {zone.nom}")
    #     plt.legend()


    plt.figure(f"Tous les producteurs dispatchables {zone.nom}")

    # Demande
    plt.plot(zone.conso, "b", label=f"Demande {zone.nom}")
    plt.plot(IntercoZone,label =f"IntercoZone")
    Niveau1 =[
        IntercoZone[h] + zone.productionFatal[h]
        for h in range(nbHeures)
    ]
    plt.fill_between(range(nbHeures),IntercoZone,Niveau1,color = 'red',label =f"Production Fatal")


    plt.show()
