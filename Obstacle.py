from Vecteur import Vecteur
class Obstacle :
    """
        Un obstacle est défini par un vecteur et est une partie de l'environnement
    """

    def __init__(self, x1, x2, y1, y2) :
        """
        Constructeur d'un obstacle
        arg x1 -> Position en x de départ du vecteur
        arg x2 -> Position en x d'arrivée du vecteur
        arg y1 -> Position en y de départ du vecteur
        arg y2 -> Position en y d'arrivée du vecteur

        Attribut d'instance d'Obstacle :
        VecteurObstacle -> Création d'une instance de la classe Vecteur avec comme attribut en x : x2-x1, en y : y2-y1
        """
        VecteurObstacle : Vecteur(x2-x1, y2-y1)