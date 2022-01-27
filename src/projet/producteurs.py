class Producteur:
    def __init__(self, zone, centrale, type, capaciteMax):
        self.type = type  # charbon, TAC, diesel, renouvelable
        self.centrale = centrale  # Bois Rouge, Le Gol, hydro, solaire...
        self.zone = zone  # Nord ou Sud
        self.capaciteMax = capaciteMax  # en MW

    def myfunc(self):
        print("Je m'appelle " + self.centrale)


tousProducteurs = [
    # Thermiques
    Producteur("Sud", "Bois Rouge", "charbon", 100),
    Producteur("Nord", "Le Gol", "charbon", 110),
    Producteur("Nord", "La Baie", "tac", 80),
    Producteur("Nord", "Le Port Est", "diesel", 216),
    # Renouvelables
    Producteur("Sud", "Hydraulique", "renouvelable", 134),
    Producteur("Sud", "Solaire Sud", "renouvelable", 115),
    Producteur("Sud", "Bioénergies", "renouvelable", 4),
    Producteur("Sud", "Eolien", "renouvelable", 16),
    Producteur("Nord", "Solaire Nord", "renouvelable", 58),
]

# Cout marginal, en € par MWh
coutMarginal = {"tac": 150, "diesel": 80, "charbon": 40, "renouvelable": 0}

capaTotale = sum([prod.capaciteMax for prod in tousProducteurs])
print(capaTotale)
