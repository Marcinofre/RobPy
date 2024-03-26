import math

class Vecteur:
    """
        Un vecteur permet de modéliser le robot (et ses mouvements) et les différents obstacles de l'environnement
    """
    def __init__(self,x,y) :
        """
            Constructeur de la classe Vecteur

            Args:
                x: Coordonnée en abcisse du vecteur
                y: Coordonnée en ordonnée du vecteur
        """
        self.x = x
        self.y = y
    
    def calcNorm(self):
        """
            Calcule la norme d'un vecteur
        """
        return (self.x**2+self.y**2)**0.5
    
    def produitVectoriel(self,other):
        """
            Calcule le produit vectoriel de deux vecteur

            Args:
                other: un autre objet de class `Vecteur`
        """
        return self.x*other.y-self.y*other.x 
    
    def produitScalaire(self, other):
        """
            Calcule le produit scalaire de deux vecteur

            Args:
                other: un autre objet de class `Vecteur` 
        """

        return self.x*other.x+self.y*other.y

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

    def rotationAngle(self, angledeg):
        """
            On tourne le vecteur d'un angle en degré donné en paramètre
        """
        # Le module math utilise des radians pour calculer le cos et le sin on convertit donc les degrés
        anglerad = math.radians(angledeg)
        # On met dans des variables temporaires les nouvelles valeurs de x et y
        newx = self.x*math.cos(anglerad) - self.y*math.sin(anglerad)
        newy = self.x*math.sin(anglerad) + self.y*math.cos(anglerad)
        # On arrondit les valeurs à 2 chiffre après la virgule
        self.x = round(newx,1)
        self.y = round(newy,1)

    def toTuple(self):
        """
            Retrourne le vecteur sous la forme d'un couple de point (x,y)
        """
        return (self.x, self.y)
    
