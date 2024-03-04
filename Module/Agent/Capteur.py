from Module.Vecteur import Vecteur
from Module.Contr.VoirObstacle import VoirObstacle
from Module.Agent.Robot import Robot as rob
from Module.Env.Environnement import Environnement as env


class Capteur :
    """
		Modélisation du capteur de mouvement du robot de Sorbonne Université
	"""

    def __init__(self, vecteurDirecteurRobot:Vecteur) -> None:
        """
             Attributs d'un capteur
                => Vecteur ray : vecteur représentant le rayon du capteur
			    => int vision : distance de vision max
                => boolean touchObstacle : indique si un obstacle touche le vecteur   -> False ( aucun obstacle )                                                                                                                                       -> True ( obsctale)
	    """
        self.ray = Vecteur(0,1)
        self.ray.rotationAngle(vecteurDirecteurRobot.calculerAngle(self.ray))
        self.vision = 8000
        self.interfaceRay = 0
        self.touchObstacle = False
        self.distanceObstacle = 0

    def getObstacle(self):
        """
            Retourne la distance entre le robot et l'obstacle si il y'en a un, sinon retourne -1
        """
        if self.e.retourCapteur(self.pas_distance):
            return self.distanceObstacle
        return -1
        


       

    
