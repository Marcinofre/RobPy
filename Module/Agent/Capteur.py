from Module.Vecteur import Vecteur

class Capteur :
    """
		Modélisation du capteur de mouvement du robot de Sorbonne Université
	"""()

    def __init__(self, ray:Vecteur, vision:int, touchObstacle:bool=False ) -> None:

        """
			Constructeur d'un capteur
			Vecteur ray	: vecteur représentant le rayon du capteur
			int vision	: distance de vision du capteur
            boolean touchObstacle : indique si un obstacle touche le vecteur   -> False ( aucun obstacle )
                                                                               -> True ( obsctale)
	    """