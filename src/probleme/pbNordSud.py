import pulp
import sys, os

# Add src to the path so that Python finds our modules
src_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(src_dir)

# Import our files
from postTraitementFiles import postTraitement
from modelisation.readExcel import nbHeures
from modelisation.zones import mesZones, ZoneName
import modelisation.ourValues as ourValues
from probleme import variables, contraintes, objectif


""" Problème version 4 """
""" Le Sud et le Nord ont des producteurs différents """
""" Il y a une interconnexion entre les deux, pour transférer de l'électricité """
""" Ce problème se déroule sur plusieurs heures, on a donc autant de données de consommation """
""" On peut allumer et éteindre des unités d'un site de production """


def main():
    # La demande
    assert (
        len(mesZones[ZoneName.SUD].conso)
        == len(mesZones[ZoneName.NORD].conso)
        == nbHeures
    )
    # On augmente un peu les consos
    for zone in mesZones.values():
        zone.conso = zone.conso * ourValues.facteurAugmentationConso

    # On crée le problème de minimisation du coût
    problem = pulp.LpProblem("NordSudAnnee", pulp.LpMinimize)

    """ Création des variables de production """
    variables.ajoutVariables(mesZones)

    """ Ajout de contraintes """
    contraintes.ajoutContraintes(mesZones, problem)

    """ Définition de l'objectif """
    objectif.ajouterObjectif(mesZones, problem)

    """ Résolution du problème """
    status = problem.solve(pulp.PULP_CBC_CMD(msg=1))
    # On vérifie que pulp arrive à trouver une solution
    assert pulp.LpStatus[status] == "Optimal"

    """ Post-traitement """
    postTraitement.traitementResultats(problem, mesZones, nbHeures)


if __name__ == "__main__":
    main()
