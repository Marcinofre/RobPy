from Module.Vecteur import Vecteur

class Capteur :
    """
		Modélisation du capteur de mouvement du robot de Sorbonne Université
	"""

    def __init__(self, vision:int) -> None:

        """
			Constructeur d'un capteur =
			    => int vision : distance de vision du capteur en mètres

            Attributs d'un capteur =
                => Vecteur ray : vecteur représentant le rayon du capteur
			    => int vision : distance de vision passée en paramètre du constructeur
                => boolean touchObstacle : indique si un obstacle touche le vecteur   -> False ( aucun obstacle )
                                                                                      -> True ( obsctale)
	    """

        self.ray = Vecteur(0, 0) 
        self.vision = vision
        self.touchObstacle = False

    def projectionRay (self,distance):
        """
            Retourne le rayon projeté à la distance passé en paramètre en mètres
        """
        return (self.ray.x * distance, self.ray.y * distance)
       

    
