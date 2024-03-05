from Module.Vecteur import Vecteur


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
        self.ray = self.treatVector(vecteurDirecteurRobot)
        self.vision = 8000 # distance max du capteur en mm
        self.interfaceRay = self.ray
        self.touchObstacle = False
        self.distanceObstacle = 0

    def projectionRay(self,distance):
        """
            Retourne le rayon projeté à la distance passé en paramètre en mètres
        """
        return (self.ray.x * distance, self.ray.y * distance)
    
    def treatVector(self, vec : Vecteur):
        res = Vecteur(0,0)
        if vec.y > 0 :
            res.y = 1
        if vec.x > 0 :
            res.x = 1
        if vec.x<0 :
            res.x = -1
        if vec.y<0 :
            res.y = -1
        return res

       

    
