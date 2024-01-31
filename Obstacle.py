from Vecteur import Vecteur
class Obstacle :
    """
        Un obstacle est une partie de l'environnement et est representé par un vecteur
    """

    def __init__(self, x0, y0, x1, y1) :
        """
        Constructeur d'un obstacle
        arg x0 -> Position en x de départ du vecteur
        arg x1 -> Position en x d'arrivée du vecteur
        arg y0 -> Position en y de départ du vecteur
        arg y1 -> Position en y d'arrivée du vecteur

        Attribut d'instance d'Obstacle :
        Vecteur -> Création d'une instance de la classe Vecteur avec comme attribut en x : x2-x1, en y : y2-y1
        """
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1