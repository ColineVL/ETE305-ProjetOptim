from readExcel import (
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
    """

    def __init__(
        self, zone, centrale, type, puissanceMax, puissanceMin=0, dureeMinAllumage=0
    ):
        self.type = type
        self.nomCentrale = centrale
        self.zone = zone
        self.puissanceMax = puissanceMax
        self.puissanceMin = puissanceMin
        self.coutMarginal = 0
        self.dureeMinAllumage = dureeMinAllumage


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
        ProducteurDispatchable("Sud", f"Bois_Rouge_{i}", "charbon", 33, 10, 6)
    )
for i in range(1, 1 + 3):
    tousProducteursDispatchables.append(
        ProducteurDispatchable("Nord", f"Le_Gol_{i}", "charbon", 37, 10, 6)
    )
for i in range(1, 1 + 3):
    tousProducteursDispatchables.append(
        ProducteurDispatchable("Nord", f"La_Baie_{i}", "tac", 40, 15, 1)
    )
for i in range(1, 1 + 3):
    tousProducteursDispatchables.append(
        ProducteurDispatchable("Nord", f"Le_Port_Est_{i}", "diesel", 18, 0, 1)
    )

# Cout marginal, en € par MWh
dataCoutMarginal = {"tac": 150, "diesel": 80, "charbon": 40}

# On calcule le cout marginal de chaque site de production
for prod in tousProducteursDispatchables:
    prod.coutMarginal = dataCoutMarginal[prod.type]

# Division Nord / Sud
producteursDispatchablesNord = []
producteursDispatchablesSud = []
for prod in tousProducteursDispatchables:
    if prod.zone == "Nord":
        producteursDispatchablesNord.append(prod)
    if prod.zone == "Sud":
        producteursDispatchablesSud.append(prod)

producteursFatalNord = []
producteursFatalSud = []
for prod in tousProducteursFatal:
    if prod.zone == "Nord":
        producteursFatalNord.append(prod)
    if prod.zone == "Sud":
        producteursFatalSud.append(prod)
