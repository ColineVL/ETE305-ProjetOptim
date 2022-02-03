class Producteur:
    """
    Représente un producteur d'électricité

    Attributes
    ----------
    zone : str
        "Nord" ou "Sud"
    centrale : str
        Nom de la centrale, sans espace : "Bois_Rouge_1", "Hydraulique"...
    type : str
        Type d'énergie : "charbon" ou "tac" ou "diesel" ou "renouvelable"
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


# Tableau regroupant tous les producteurs
tousProducteurs = [
    # Renouvelables
    Producteur("Sud", "Hydraulique", "renouvelable", 134),
    Producteur("Sud", "Solaire_Sud", "renouvelable", 115),
    Producteur("Sud", "Bioenergies", "renouvelable", 4),
    Producteur("Sud", "Eolien", "renouvelable", 16),
    Producteur("Nord", "Solaire_Nord", "renouvelable", 58),
]

# On ajoute les thermiques : dans chaque site de production, il y a plusieurs groupes qui peuvent être activés indépendamment les uns des autres.
# Dans le range, le 1+3 signifie qu'il y a 3 groupes dans ce site de production
for i in range(1, 1 + 3):
    tousProducteurs.append(Producteur("Sud", f"Bois_Rouge_{i}", "charbon", 33, 10, 6))
for i in range(1, 1 + 3):
    tousProducteurs.append(Producteur("Nord", f"Le_Gol_{i}", "charbon", 37, 10, 6))
for i in range(1, 1 + 3):
    tousProducteurs.append(Producteur("Nord", f"La_Baie_{i}", "tac", 40, 15, 1))
for i in range(1, 1 + 3):
    tousProducteurs.append(Producteur("Nord", f"Le_Port_Est_{i}", "diesel", 18, 0, 1))

# Cout marginal, en € par MWh
dataCoutMarginal = {"tac": 150, "diesel": 80, "charbon": 40, "renouvelable": 0}

# On calcule le cout marginal de chaque site de production
for prod in tousProducteurs:
    prod.coutMarginal = dataCoutMarginal[prod.type]

# Juste en rappel
capaTotale = sum([prod.puissanceMax for prod in tousProducteurs])


# Division Nord / Sud
producteursNord = []
producteursSud = []
for prod in tousProducteurs:
    if prod.zone == "Nord":
        producteursNord.append(prod)
    if prod.zone == "Sud":
        producteursSud.append(prod)
