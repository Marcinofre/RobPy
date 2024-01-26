import math
class Vecteur:
    """
        Un vecteur permet de modéliser le robot (et ses mouvements) et les différents obstacles de l'environnement
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
    
    
    def produitVectoriel(self,other):
        """
            Calculer le produit vectoriel de deux vecteur 
        """
        return self.x*other.y-self.y*self.x 
    

    def produitScalaire(self, other):
        """
            Calculer le produit Scalaire de deux vecteur
        """

        return self.x*other.x+self.y*other.y

    #Code a revoir, ne passe pas les tests
    def calculerAngle(self,other):
        """
            Calculer l'angle en degree entre 2 differents vecteur
        """

        prod_scalaire=self.produitScalaire(other)
        norme1=self.calcNorm()
        norme2=other.calcNorm()
        #calculer Cos
        cos_2vect=prod_scalaire/(norme1+norme2)
        #calculer Acos(cos)
        angleParRadians=math.acos(cos_2vect) # --> leve un valueError : math domain error
        angleParDegree=math.degrees(angleParRadians)
        return angleParDegree
    

    def rotationAngle(self, angle):
        """
            On tourne le vecteur d'un angle 
        """
        anglerad = math.radians(angle)
        newx = self.x*math.cos(anglerad) - self.y*math.sin(anglerad)
        newy = self.x*math.sin(anglerad) + self.y*math.cos(anglerad)
        self.x = newx
        self.y = newy