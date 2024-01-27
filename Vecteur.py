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

    #Un petit soucis, lorsque le produit vect est 0 l'angle = 90 donc si tu as un vecteur (0,0) il doit retourner 90
    def calculerAngle(self,other):
        """
            Calculer l'angle en degree entre 2 differents vecteur
        """

        prod_scalaire=self.produitScalaire(other)
        norme1=self.calcNorm()
        norme2=other.calcNorm()
        if (self.produitScalaire(other)==0):
            return 90
        #calculer Cos
        cos_2vect=max(min((prod_scalaire/(norme1*norme2)), 1), -1)#L'intervalle accepté pour Acos est [-1, 1], valeur de cosinus doit entre [-1,1]
        #calculer Acos(cos)

        angleParRadians=math.acos(cos_2vect) 
        angleParDegree=math.degrees(angleParRadians)
        if (angleParDegree-int(angleParDegree)<=0.5):
            return math.floor(angleParDegree)
        else:
            return math.ceil(angleParDegree)

    def rotationAngle(self, angle):
        """
            On tourne le vecteur d'un angle 
        """
        anglerad = math.radians(angle)
        newx = self.x*math.cos(anglerad) - self.y*math.sin(anglerad)
        self.y = self.x*math.sin(anglerad) + self.y*math.cos(anglerad)
        self.x = newx