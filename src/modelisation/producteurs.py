from modelisation.enums import TypeEnergie, ZoneName
from modelisation.readExcel import (
    prodSolaireNord,
    prodSolaireSud,
    prodEolienSud,
    prodHydroSud,
    prodBioenergiesSud,
)


class ProducteurDispatchable:
    """
    Représente un producteur d'électricité d'origine fossile, dispatchable

    Attributes
    ----------
    zone : ZoneName
        Nord ou Sud
    nomCentrale : str
        Nom de la centrale, sans espace : "Bois_Rouge_1", "La Baie"...
    type : TypeEnergie
        Type d'énergie : charbon ou tac ou diesel
    puissanceMax : int
        Puissance maximale de la centrale, en MW
    puissanceMin : int
        Puissance minimale de la centrale, en MW
    dureeMinAllumage : int
        Durée minimale d'allumage de la centrale, en heures.
        Si on allume la centrale, elle doit rester allumer pendant un certain temps
    coutMarginal : int
        Cout d'utilisation de la centrale par mégawatt et par heure, donc en € / MWh
    coutAllumage : int
        Cout d'allumage de la centrale, en €
    variablesProduction : array[pulp.LpVariable]
        Tableau de variables pulp : variablesProduction[h] = production à l'heure h
    variablesOnOff : array[pulp.LpVariable]
        Tableau de variables pulp binaires : variablesOnOff[h] = True => à l'heure h l'usine est allumée
    solutionProduction : array[float]
        Rempli après la résolution du problème. Quantité de production à chaque heure
    """

    def __init__(
        self,
        zone,
        nomCentrale,
        type,
        puissanceMax,
        puissanceMin,
        dureeMinAllumage,
        coutAllumage,
    ):
        self.type = type
        self.nomCentrale = nomCentrale
        self.zone = zone
        self.puissanceMax = puissanceMax
        self.puissanceMin = puissanceMin
        self.coutMarginal = type.value
        self.dureeMinAllumage = dureeMinAllumage
        self.variablesProduction = []
        self.variablesOnOff = []
        self.solutionProduction = []
        self.coutAllumage = coutAllumage

    def calculerCoutProduction(self):
        return sum(self.variablesProduction) * self.coutMarginal

    def donnerMeilleursTypes(self):
        return self.type.meilleursTypes()


class ProducteurFatal:
    """
    Représente un producteur d'électricité d'origine renouvelable.
    On ne peut pas choisir la production, elle est donnée (par les conditions climatiques par exemple)

    Attributes
    ----------
    zone : ZoneName
        Nord ou Sud
    centrale : str
        Nom de la centrale, sans espace : "Hydraulique", "Solaire"...
    type : TypeEnergie
        Type d'énergie : HYDRO ou EOLIEN ou BIOENERGIES ou SOLAIRE
    production : array
        Production au cours du temps, heure par heure
    """

    def __init__(self, zone, centrale, type, production):
        self.nomCentrale = centrale
        self.zone = zone
        self.type = type
        self.production = production


""" Il est temps de créer nos producteurs"""

# Tableau regroupant tous les producteurs, d'abord ceux d'origine fatal
tousProducteurs = [
    ProducteurFatal(ZoneName.SUD, "Hydraulique", TypeEnergie.HYDRO, prodHydroSud),
    ProducteurFatal(ZoneName.SUD, "Solaire_Sud", TypeEnergie.SOLAIRE, prodSolaireSud),
    ProducteurFatal(
        ZoneName.SUD, "Bioenergies", TypeEnergie.BIOENERGIES, prodBioenergiesSud
    ),
    ProducteurFatal(ZoneName.SUD, "Eolien", TypeEnergie.EOLIEN, prodEolienSud),
    ProducteurFatal(
        ZoneName.NORD, "Solaire_Nord", TypeEnergie.SOLAIRE, prodSolaireNord
    ),
]

# On ajoute les dispatchables
# Dans chaque site de production, il y a plusieurs groupes qui peuvent être activés indépendamment les uns des autres.
# Dans le range, le 1+3 signifie qu'il y a 3 groupes dans ce site de production
def creer(nombre, zone, nom, *autres):
    for i in range(1, 1 + nombre):
        tousProducteurs.append(ProducteurDispatchable(zone, f"{nom}_{i}", *autres))


creer(3, ZoneName.SUD, "Bois_Rouge", TypeEnergie.CHARBON, 33, 10, 6, 50000)
creer(3, ZoneName.NORD, "Le_Gol", TypeEnergie.CHARBON, 37, 10, 6, 50000)
creer(2, ZoneName.NORD, "La_Baie", TypeEnergie.TAC, 40, 15, 1, 2000)
creer(12, ZoneName.NORD, "Le_Port_Est", TypeEnergie.DIESEL, 18, 0, 1, 1000)
