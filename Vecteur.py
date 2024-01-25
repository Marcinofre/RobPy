class Vecteur:
    """
        Un vecteur permet de modéliser le robot et ses mouvements, et les différents obstacles de l'environnement
    """
    def __init__(self,x,y) :
        """
            Constructeur de la classe Vecteur :
            arg x  ->  Coordonnée en abcisse du vecteur
            arg y  ->  Coordonnée en ordonnée du vecteur
        """
        self.x = x
        self.y = y
    
    def calcNorm(self):
        """
            Permet de calculer la norme d'un vecteur
        """
        return (self.x**2+self.y**2)**0.5