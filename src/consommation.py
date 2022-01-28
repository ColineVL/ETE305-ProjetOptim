import numpy as np

""" Consommation en MW """

consoNord = 217
consoSud = 265

consoTotale = consoNord + consoSud

demand = np.loadtxt("./src/demand.txt")
consoJournee = demand[:24]
