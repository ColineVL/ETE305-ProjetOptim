from enum import Enum, auto


class ZoneName(Enum):
    """Nom de zone"""

    NORD = auto()
    SUD = auto()


class TypeEnergie(Enum):
    """Types d'énergie, le coût est différent selon le type"""

    TAC = 150
    DIESEL = 80
    CHARBON = 40
    SOLAIRE = 0
    HYDRO = 0
    EOLIEN = 0
    BIOENERGIES = 0

    def meilleursTypes(self):
        return [
            type
            for type in [TypeEnergie.TAC, TypeEnergie.DIESEL, TypeEnergie.CHARBON]
            if type.value < self.value
        ]
