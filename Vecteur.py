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
    

    def produitScalaire(self,other):
        """
            Calculer le produit Scalaire de deux vecteur
        """

        return self.x*other.x-self.y*other.y


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
        angleParRadians=math.acos(cos_2vect)
        angleParDegree=math.degrees(angleParRadians)
        return angleParDegree
    

    def rotation1vecteur(self,angle_degree):
        """
            Rotation un vecteur par un point fixé
        """
        #radians=angle_degree*(pi/180)
        angleParRadians=math.radians(angle_degree)
        #newX = x*cos(radians)-y*sin(radians)
        newX=self.x*math.cos(angleParRadians)-self.y*math.sin(angleParRadians)
        #newY = x*sin(radians)+y*cos(radians)
        newY=self.x*math.sin(angleParRadians)-self.y*math.cos(angleParRadians)
        return Vecteur(newX,newY)
    


