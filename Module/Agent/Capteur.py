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
        # =======> A faire
        

    def RayTouchObsctacle (self):
        """
            Projection du rayon qui s'incrémente jusqu'à détécter un obstacle
        """
        # Initialisition de la projection du rayon à 1cm
        projection = 0.01 
        # Tant que la projection est dans la vision et qu'aucun obstacle ne touche le vecteur du rayon 
        while (self.vision < projection) and ( not self.agent.capteur.touchObstacle): 
            # Si un obstacle est détécté 
            if self.doesRayTouch(self.ray):
                # On sort de la boucle en mettant à jour l'attribut touchObstacle
                self.agent.capteur.touchObstacle = True
                # On retourne la projection pour connaître la distance entre le robot et l'obstacle
                return projection
            # Si aucun obstacle est détécté
            else:
                # Incrémentation de la projection du rayon de 1cm
                projection = projection + 0.01  
                # Mise à jour de la projection du rayon du capteur
                self.agent.capteur.projectionRay(projection)
        return -1


       

    
