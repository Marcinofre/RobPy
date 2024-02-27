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
    
    def doesRayTouch (self,ray):
        """
            Retourne un boolean qui dis si le rayon touche un obstacle
        """
        # A faire

    def RayTouchObsctacle (self):
        """
            Projection du rayon qui s'incrémente jusqu'à détécter un obstacle
        """
        projection = 0.01 # Initialisition de la projection du rayon à 1cm
        while (self.vision < projection) and ( not self.agent.capteur.touchObstacle): 
            if self.doesRayTouch(self.ray):
                self.agent.capteur.touchObstacle = True
                return projection
            else:
                projection = projection + 0.01  # Incrémentation de la projection du rayon de 1cm
                self.agent.capteur.projectionRay(projection)
        return -1


       

    
