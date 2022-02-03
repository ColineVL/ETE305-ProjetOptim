import numpy as np

""" Consommation en MW """

consoNord = 217
consoSud = 265

consoTotale = consoNord + consoSud

demand = np.loadtxt("./src/demand.txt")
consoJournee = demand[:24]
# On l'augmente sinon on voit aucun effet des fossiles
for i in range(len(consoJournee)):
    consoJournee[i] += 300

demandNord = np.loadtxt("./src/demandNord.txt")
demandSud = np.loadtxt("./src/demandSud.txt")
consoJourneeNord = demandNord[:24]
consoJourneeSud = demandSud[0:24]
