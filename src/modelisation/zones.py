from modelisation.enums import ZoneName
from modelisation.producteurs import ProducteurDispatchable, tousProducteurs
from modelisation.readExcel import consoNord, consoSud, nbHeures


class Zone:
    """
    Représente une zone, Nord ou Sud

    Attributes
    ----------
    nom : ZoneName
        Nord ou Sud
    producteursDispatchable : array
        Tableau des producteurs de dispatchable de cette zone, de type ProducteurDispatchable
    producteursFatal : array
        Tableau des producteurs de fatal de cette zone, de type ProducteurFatal
    conso : array
        Tableau de la consommation dans cette zone, heure par heure
    capaciteIntercoVersMoi : pulp.LpVariable
        Capacité de l'interconnexion de l'autre zone vers moi
    intercoVersMoi : array[pulp.LpVariable]
        Tableau de variables pulp : intercoVersMoi[h] = ce que m'envoie l'autre zone à l'heure h
    solutionCapaciteIntercoVersMoi : float
        Solution de capacité de l'interconnexion de l'autre zone vers moi
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

    def __repr__(self):
        return f"{self.nom}"

    def calculerCoutProductionZone(self):
        return sum(
            prod.calculerCoutProduction() for prod in self.producteursDispatchable
        )

    def autreZone(self):
        """Retourne l'autre zone : Sud si self == Nord"""
        return ZoneName.SUD if self.nom == ZoneName.NORD else ZoneName.NORD


mesZones = {
    ZoneName.NORD: Zone(ZoneName.NORD, consoNord),
    ZoneName.SUD: Zone(ZoneName.SUD, consoSud),
}

# Division Nord / Sud des producteurs
for prod in tousProducteurs:
    zone = mesZones[prod.zone]
    if isinstance(prod, ProducteurDispatchable):
        zone.producteursDispatchable.append(prod)  # C'est un dispatchable
    else:
        zone.producteursFatal.append(prod)  # C'est un fatal
