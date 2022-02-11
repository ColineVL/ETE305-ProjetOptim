from producteurs import tousProducteurs
from readExcel import consoNord, consoSud
from bornesMax import facteurAugmentationConso

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
    productionFatal : array[float]
        Total à chaque heure des productions de fatal
    conso : array
        Tableau de la consommation dans cette zone, heure par heure
    capaciteIntercoVersMoi : pulp.LpVariable
        Capacité de l'interconnexion de l'autre zone vers moi
    intercoVersMoi : array[pulp.LpVariable]
        Tableau de variables pulp : intercoVersMoi[h] = ce que m'envoie l'autre zone à l'heure h
    solutionIntercoVersMoi : array[float]
        Tableau flottants, valeur de l'interco à chaque h
    """

    def __init__(self, nom, conso):
        self.nom = nom
        self.producteursDispatchable = []
        self.producteursFatal = []
        self.conso = conso
        self.intercoVersMoi = []
        self.solutionIntercoVersMoi = []
        self.productionFatal = []

    def calculerCoutProductionZone(self):
        return sum(
            prod.calculerCoutProduction() for prod in self.producteursDispatchable
        )

    def calculerProductionFatal(self):
        self.productionFatal = [
            sum(
                prod.production[h] for prod in self.producteursFatal
            )
        ]


zoneNord = Zone("Nord", consoNord*facteurAugmentationConso)
zoneSud = Zone("Sud", consoSud*facteurAugmentationConso)
mesZones = {"Nord": zoneNord, "Sud": zoneSud}

# Division Nord / Sud des producteurs
for prod in tousProducteurs:
    zone = mesZones[prod.zone]
    if hasattr(prod, "type"):
        zone.producteursDispatchable.append(prod)  # C'est un dispatchable
    else:
        zone.producteursFatal.append(prod)  # C'est un fatal

# Calcul fatal
for zone in mesZones:
    zone.calculerProductionFatal()