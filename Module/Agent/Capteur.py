from Module.Vecteur import Vecteur

class Capteur :
    """
		Modélisation du capteur de mouvement du robot de Sorbonne Université
	"""

    def __init__(self, vecteurDirecteurRobot:Vecteur) -> None:

        """
             Attributs d'un capteur
                => Vecteur ray : vecteur représentant le rayon du capteur
			    => int vision : distance de vision passée en paramètre du constructeur
                => boolean touchObstacle : indique si un obstacle touche le vecteur   -> False ( aucun obstacle )
                                                                                      -> True ( obsctale)
	    """

        self.ray = Vecteur(0,1)
        self.ray.rotationAngle(vecteurDirecteurRobot.calculerAngle(self.ray))
        self.interfaceRay = self.ray
        self.vision = 500
        self.touchObstacle = False
        
        self.distanceObstacle = 0

    def projectionRay(self,distance):
        """
            Retourne le rayon projeté à la distance passé en paramètre en mètres
        """
        return (self.ray.x * distance, self.ray.y * distance)
    


       

    
