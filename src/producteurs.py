from readExcel import (
    prodSolaireNord,
    prodSolaireSud,
    prodEolienSud,
    prodHydroSud,
    prodBioenergiesSud,
)

dataCoutMarginal = {"tac": 150, "diesel": 80, "charbon": 40}


class ProducteurDispatchable:
    """
    Représente un producteur d'électricité d'origine fossile, dispatchable

    Attributes
    ----------
    zone : str
        "Nord" ou "Sud"
    centrale : str
        Nom de la centrale, sans espace : "Bois_Rouge_1", "La Baie"...
    type : str
        Type d'énergie : "charbon" ou "tac" ou "diesel"
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
        centrale,
        type,
        puissanceMax,
        puissanceMin,
        dureeMinAllumage,
        coutAllumage,
    ):
        self.type = type
        self.nomCentrale = centrale
        self.zone = zone
        self.puissanceMax = puissanceMax
        self.puissanceMin = puissanceMin
        self.coutMarginal = dataCoutMarginal[type]
        self.dureeMinAllumage = dureeMinAllumage
        self.variablesProduction = []
        self.variablesOnOff = []
        self.solutionProduction = []
        self.coutAllumage = coutAllumage

    def calculerCoutProduction(self):
        return sum(self.variablesProduction) * self.coutMarginal

    def donnerMeilleursTypes(self):
        return [
            type
            for type in dataCoutMarginal
            if dataCoutMarginal[type] < self.coutMarginal
        ]


class ProducteurFatal:
    """
    Représente un producteur d'électricité d'origine renouvelable.
    On ne peut pas choisir la production, elle est donnée (par les conditions climatiques par exemple)

    Attributes
    ----------
    zone : str
        "Nord" ou "Sud"
    centrale : str
        Nom de la centrale, sans espace : "Hydraulique", "Solaire"...
    production : array
        Production au cours du temps, heure par heure
    """

    def __init__(self, zone, centrale, production):
        self.nomCentrale = centrale
        self.zone = zone
        self.production = production


""" Il est temps de créer nos producteurs"""

# Tableau regroupant tous les producteurs d'origine fatal
tousProducteursFatal = [
    ProducteurFatal("Sud", "Hydraulique", prodHydroSud),
    ProducteurFatal("Sud", "Solaire_Sud", prodSolaireSud),
    ProducteurFatal("Sud", "Bioenergies", prodBioenergiesSud),
    ProducteurFatal("Sud", "Eolien", prodEolienSud),
    ProducteurFatal("Nord", "Solaire_Nord", prodSolaireNord),
]

# Tableau regroupant tous les producteurs dispatchables
tousProducteursDispatchables = []
# Dans chaque site de production, il y a plusieurs groupes qui peuvent être activés indépendamment les uns des autres.
# Dans le range, le 1+3 signifie qu'il y a 3 groupes dans ce site de production
for i in range(1, 1 + 3):
    tousProducteursDispatchables.append(
        ProducteurDispatchable("Sud", f"Bois_Rouge_{i}", "charbon", 33, 10, 6, 50000)
    )
for i in range(1, 1 + 3):
    tousProducteursDispatchables.append(
        ProducteurDispatchable("Nord", f"Le_Gol_{i}", "charbon", 37, 10, 6, 50000)
    )
for i in range(1, 1 + 3):
    tousProducteursDispatchables.append(
        ProducteurDispatchable("Nord", f"La_Baie_{i}", "tac", 40, 15, 1, 2000)
    )
for i in range(1, 1 + 3):
    tousProducteursDispatchables.append(
        ProducteurDispatchable("Nord", f"Le_Port_Est_{i}", "diesel", 18, 0, 1, 1000)
    )
