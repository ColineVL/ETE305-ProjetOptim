class Producteur:
    def __init__(self, zone, centrale, type, puissanceMax, puissanceMin):
        self.type = type  # charbon, TAC, diesel, renouvelable
        self.nomCentrale = centrale  # Bois Rouge, Le Gol, hydro, solaire...
        self.zone = zone  # Nord ou Sud
        self.puissanceMax = puissanceMax  # en MW
        self.puissanceMin = puissanceMin  # en MW
        self.coutMarginal = 0  # en € / MWh

    def myfunc(self):
        print("Je m'appelle " + self.centrale)


# Tableau regroupant tous les producteurs
tousProducteurs = [
    # Renouvelables
    Producteur("Sud", "Hydraulique", "renouvelable", 134, 0),
    Producteur("Sud", "Solaire_Sud", "renouvelable", 115, 0),
    Producteur("Sud", "Bioenergies", "renouvelable", 4, 0),
    Producteur("Sud", "Eolien", "renouvelable", 16, 0),
    Producteur("Nord", "Solaire_Nord", "renouvelable", 58, 0),
]

# On ajoute les thermiques : dans chaque site de production, il y a plusieurs groupes qui peuvent être activés indépendamment les uns des autres.
# Dans le range, le 1+3 signifie qu'il y a 3 groupes dans ce site de production
for i in range(1, 1 + 3):
    tousProducteurs.append(Producteur("Sud", f"Bois_Rouge_{i}", "charbon", 33, 10))
for i in range(1, 1 + 3):
    tousProducteurs.append(Producteur("Nord", f"Le_Gol_{i}", "charbon", 37, 10))
for i in range(1, 1 + 3):
    tousProducteurs.append(Producteur("Nord", f"La_Baie_{i}", "tac", 40, 15))
for i in range(1, 1 + 3):
    tousProducteurs.append(Producteur("Nord", f"Le_Port_Est_{i}", "diesel", 18, 0))

# Cout marginal, en € par MWh
dataCoutMarginal = {"tac": 150, "diesel": 80, "charbon": 40, "renouvelable": 0}

# On calcule le cout marginal de chaque site de production
for prod in tousProducteurs:
    prod.coutMarginal = dataCoutMarginal[prod.type]

# Juste en rappel
capaTotale = sum([prod.puissanceMax for prod in tousProducteurs])
