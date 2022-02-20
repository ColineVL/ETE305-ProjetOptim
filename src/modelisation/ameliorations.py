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
    borneMax : float
        Valeur maximale de la capacité
    capaciteInitiale : float
       Valeur initiale de la capacité
    """

    def __init__(self, zone, type, coutInvestissement, borneMax, capaciteInitiale=0):
        self.zone = zone
        self.type = type
        self.coutInvestissement = coutInvestissement
        self.borneMax = borneMax
        self.capaciteInitiale = capaciteInitiale

    def __repr__(self):
        return f"{self.zone} {self.type} {self.borneMax}"

    def __str__(self):
        return f"{self.zone} {self.type} {self.borneMax}"


ameliorations = [
    Amelioration(ZoneName.NORD, TypeEnergie.SOLAIRE, 4.8415086 * 10**6, 153, 58),
    Amelioration(ZoneName.SUD, TypeEnergie.SOLAIRE, 4.8415086 * 10**6, 305, 115),
    Amelioration(ZoneName.SUD, TypeEnergie.EOLIEN, 2.26941 * 10**6, 42, 16),
    # Et maintenant les dispatchables
    Amelioration(ZoneName.NORD, TypeEnergie.CHARBON, 2.2734171 * 10**6, 0, 0),
    Amelioration(ZoneName.NORD, TypeEnergie.TAC, 1.169256 * 10**6, 0, 0),
    Amelioration(ZoneName.SUD, TypeEnergie.CHARBON, 2.2734171 * 10**6, 0, 0),
    Amelioration(ZoneName.SUD, TypeEnergie.TAC, 1.169256 * 10**6, 0, 0),
]
