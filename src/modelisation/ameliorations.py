from modelisation.enums import ZoneName, TypeEnergie


class Amelioration:
    """
    Représente une amélioration possible, pour un type d'énergie et une zone

    Attributes
    ----------
    type : TypeEnergie
        Type d'énergie : HYDRO ou EOLIEN par exemple
    zone : ZoneName
        Nom de la zone concernée, NORD ou SUD
    coutInvestissement : float
        Cout d'investissement, en € par MW
    """

    def __init__(self, zone, type, coutInvestissement):
        self.zone = zone
        self.type = type
        self.coutInvestissement = coutInvestissement

    def __repr__(self):
        return f"{self.zone} {self.type}"

    def __str__(self):
        return f"{self.zone} {self.type}"


class AmeliorationFatal(Amelioration):
    """
    Représente une amélioration possible, pour un type d'énergie fatal et une zone

    Attributes
    ----------
    borneMax : float
        Valeur maximale de la capacité
    capaciteInitiale : float
       Valeur initiale de la capacité
    capacite : pulp.LpVariable
        On peut améliorer la capacité du producteur : nouvelle capa en MW
    """

    def __init__(self, zone, type, coutInvestissement, borneMax, capaciteInitiale):
        super().__init__(zone, type, coutInvestissement)
        self.borneMax = borneMax
        self.capaciteInitiale = capaciteInitiale


class AmeliorationDispatchable(Amelioration):
    """
    Représente une amélioration possible, pour un type d'énergie dispatchable et une zone

    Attributes
    ----------
    centraleConstruite : pulp.LpVariable
        True si la centrale a été construite
    """

    def __init__(self, zone, type, coutInvestissement):
        super().__init__(zone, type, coutInvestissement)


amlSolaireNord = AmeliorationFatal(
    ZoneName.NORD, TypeEnergie.SOLAIRE, 4.8415086 * 10**6, 153, 58
)


amlSolaireSud = AmeliorationFatal(
    ZoneName.SUD, TypeEnergie.SOLAIRE, 4.8415086 * 10**6, 305, 115
)

amlEolienSud = AmeliorationFatal(
    ZoneName.SUD, TypeEnergie.EOLIEN, 2.26941 * 10**6, 42, 16
)

# Et maintenant les dispatchables
amlCharbonNord = AmeliorationDispatchable(
    ZoneName.NORD, TypeEnergie.CHARBON, 2.2734171 * 10**6
)

amlTacNord = AmeliorationDispatchable(
    ZoneName.NORD, TypeEnergie.TAC, 1.169256 * 10**6
)

amlCharbonSud = AmeliorationDispatchable(
    ZoneName.SUD, TypeEnergie.CHARBON, 2.2734171 * 10**6
)

amlTacSud = AmeliorationDispatchable(ZoneName.SUD, TypeEnergie.TAC, 1.169256 * 10**6)
