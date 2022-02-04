from producteurs import tousProducteursDispatchables, tousProducteursFatal
from readExcel import (
    consoNord,
    consoSud,
    capaciteIntercoNordSud,
    capaciteIntercoSudNord,
)


class Zone:
    """
    Représente une zone, Nord ou Sud

    Attributes
    ----------
    nom : str
        "Nord" ou "Sud"
    producteursDispatchable : array
        Tableau des producteurs de dispatchable de cette zone, de type ProducteurDispatchable
    producteursFatal : array
        Tableau des producteurs de fatal de cette zone, de type ProducteurFatal
    conso : array
        Tableau de la consommation dans cette zone, heure par heure
    capaciteIntercoVersMoi : int
        Capacité de l'interconnexion de l'autre zone vers moi
    intercoVersMoi : array[pulp.LpVariable]
        Tableau de variables pulp : intercoVersMoi[h] = ce que m'envoie l'autre zone à l'heure h
    """

    def __init__(self, nom, conso, capaciteIntercoVersMoi):
        self.nom = nom
        self.producteursDispatchable = []
        self.producteursFatal = []
        self.conso = conso
        self.capaciteIntercoVersMoi = capaciteIntercoVersMoi
        self.intercoVersMoi = []

    def calculerCoutProductionZone(self):
        return sum(
            prod.calculerCoutProduction() for prod in self.producteursDispatchable
        )


zoneNord = Zone("Nord", consoNord, capaciteIntercoSudNord)
zoneSud = Zone("Sud", consoSud, capaciteIntercoNordSud)
mesZones = {"nord": zoneNord, "sud": zoneSud}

# Division Nord / Sud des producteurs
for prod in tousProducteursDispatchables:
    if prod.zone == "Nord":
        zoneNord.producteursDispatchable.append(prod)
    if prod.zone == "Sud":
        zoneSud.producteursDispatchable.append(prod)

for prod in tousProducteursFatal:
    if prod.zone == "Nord":
        zoneNord.producteursFatal.append(prod)
    if prod.zone == "Sud":
        zoneSud.producteursFatal.append(prod)
