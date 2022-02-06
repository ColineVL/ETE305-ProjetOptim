from zone import mesZones
from readExcel import nbHeures

# On vérifie que chaque heure il y a moyen de répondre à la demande

for h in range(nbHeures):
    capaciteDispNord = sum(
        prod.puissanceMax for prod in mesZones["nord"].producteursDispatchable
    )
    capaciteDispSud = sum(
        prod.puissanceMax for prod in mesZones["sud"].producteursDispatchable
    )
    productionFatalNord = sum(
        prod.production[h] for prod in mesZones["nord"].producteursFatal
    )
    productionFatalSud = sum(
        prod.production[h] for prod in mesZones["sud"].producteursFatal
    )
    totalNord = capaciteDispNord + productionFatalNord
    totalSud = capaciteDispSud + productionFatalSud

    demandeNord = mesZones["nord"].conso[h]
    demandeSud = mesZones["sud"].conso[h]

    if totalSud >= demandeSud and totalNord >= demandeNord:
        # premier cas : pas besoin d'interconnexion
        ok = 1

    elif totalSud <= demandeSud and totalNord >= demandeNord:
        # deuxieme cas : le Nord est ok mais le Sud est pas suffisant
        # On vérifie que l'interconnexion suffit à combler le déficit
        deficit = demandeSud - totalSud
        surplus = totalNord - demandeNord
        if surplus > mesZones["sud"].capaciteIntercoVersMoi:
            surplus = mesZones["sud"].capaciteIntercoVersMoi
        if surplus >= deficit:
            # c'est validé
            ok = 1
        else:
            print(f"Ici le Sud est trop déficitaire ! Heure = {h}")
            print(f"Total Nord = {totalNord}")
            print(f"surplus = {surplus}")
            print(f"Deficit : {deficit}")

    elif totalSud >= demandeSud and totalNord <= demandeNord:
        # troisieme cas : le Sud est ok mais le Nord est pas suffisant
        # On vérifie que l'interconnexion suffit à combler le déficit
        surplus = demandeSud - totalSud
        deficit = totalNord - demandeNord
        if surplus > mesZones["nord"].capaciteIntercoVersMoi:
            surplus = mesZones["nord"].capaciteIntercoVersMoi
        if surplus >= deficit:
            # c'est validé
            ok = 1
        else:
            print(f"Ici le Nord est trop déficitaire ! Heure = {h}")

    elif totalSud <= demandeSud and totalNord <= demandeNord:
        # quatrieme cas : les deux sont pas suffisants
        print(f"C'est la dèche les deux sont déficitaires ! Heure = {h}")

    else:
        # Dernier cas : un truc que j'ai pas prévu
        print(f"Ici c'était pas prévu : {h}")
