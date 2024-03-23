from Agent.robot import Robot
from Agent.robot import Capteur
from utils.vecteur import Vecteur
import math
import time


class robotFake:
    """
        Représentation factice du Robot irl et de ses fonctions
    """
    def __init__(self) -> None:
        """Initialisation du robot factice

            Args:
                x: Position en x du robot
                y: Position en y du robot
                vectD: Vecteur directeur représentant la direction que prend le robot

            Attributes:
                MOTOR_LEFT: Correspond au moteur gauche du robot
                MOTOR_RIGHT: Correspond au moteur gauche du robot
                posCenter: Position du centre du robot
                rayon: Rayon de la roue ?
                rotation: Rotation initiale du robot vis-a-vis du plan 

        """

        self.MOTOR_LEFT = 1
        self.MOTOR_RIGHT = 2

    def set_motor_dps(self, port, dps) -> None:
        """
            Définit la vitesse `dps` d'un moteur choisit selon le `port`
            
            Args:

                port: Port sur lequel on communique
                dps: Vitesse de rotation du moteur
        """
        if port == 1:
            print(f"Je met la vitesse du moteur gauche à {dps}")
        elif port == 2:
            print(f"Je met la vitesse du moteur droit à {dps}")
    
    def get_distance(self) -> None:
        pass

class robotAdapteur():
    """
        Classe permettant de communiquer avec un autre robot que le robot simulé. Plus précisément, cet adaptateur permet de communiquer avec le robot IRL
    """

    def __init__(self, robotFake):
        """
            Initialisation de l'adaptateur pour le robot IRL

            Args:
                width: Largeur du robot
                length: Longueur du robot
                x: Position du robot en x
                y: Position du robot en y
                vectD: Vecteur directeur représentant la direction que prend le robot par défaut (0,-1)

            Attributes:
                rob: Instance de robotFake

            

        """
        self.rob = robotFake
        self.posCenter = (250,250)
        self.MoteurG = 0
        self.MoteurD = 0
        self.rayon = 1
        self.vectD = Vecteur(0,1)
        self.rotation = self.vectD.calculerAngle(Vecteur(0,1))
        self.last_update = time.time()
        self._dim = [30,45]
        self.capteur = self.capteur = Capteur(self.vectD)

    def setVitesseRoue(self, d:"int | float", g:"int | float"):
        """
            Définit les vitesses des moteurs

            Args:
                d: Vitesse du moteur droit
                g: Vitesse du moteur gauche
        """
        self.MoteurD = d
        self.MoteurG = g
        self.rob.set_motor_dps(self.rob.MOTOR_LEFT, g)
        self.rob.set_motor_dps(self.rob.MOTOR_RIGHT, d)

    def get_distance_parcourue(self, deltat):
        return self.calcVitesseMoyenne() * deltat

    def get_time_passed(self):
        time_passed = self.last_update - time.time()
        self.last_update = time.time()
        return time_passed
    
    def VitesseAngulaire(self) -> float:
        """
			Permet de faire tourner le vecteur direction quand une roue va plus vite que l'autre.

            Returns:
                Renvoie l'angle de rotation induit par la vitesse des roue en degré (arrondie au 5eme chiffre significatif)
		"""
        diff = self.MoteurD - self.MoteurG
        angle = diff / self.rayon
        angle = angle * (180/math.pi)
        return round(angle,5)

    def avancerRobot(self, deltat) -> None:
        """
			Met à jour la position du robot en le faisant avancer en fonction de la vitesse et du vecteur direction
		"""
        vit = self.calcVitesseMoyenne()
        self.posCenter = (round(self.posCenter[0] + (self.vectD.x * vit*deltat), 1), round(self.posCenter[1] + (self.vectD.y * vit*deltat), 1))
        print(f"J'ai une vitesse de {vit} et je suis à {self.posCenter[0]} {self.posCenter[1]}")

    def calcVitesseMoyenne(self) :
        """
            Calcule la vitesse moyenne du Robot en fonction de la vitesse des ses moteurs
        """
        return round((self.MoteurD + self.MoteurG)/2,2)

    def rotateAllVect(self, angle:float) :
        """
			Rotation en degré du vecteur directeur et du vecteur unitaire du capteur du robot

            Args:

                angle: Angle de rotation à appliquer en degré
		"""
        self.vectD.rotationAngle(angle)
        self.rotation += angle
    
    def update(self, deltat):
        """
            Mise à jour du vecteur directeur et la position du robot
        """
        deltat = self.get_time_passed()
        self.rotateAllVect(self.VitesseAngulaire()*deltat)
        self.avancerRobot(deltat)
    
    def getCarcasse(self) -> list[tuple["int|float", "int|float"]]: 
        """Calcule les coordonnées des 4 points du robot en fonction de l'angle du robot

			Returns:
				Une liste de tuple correspondant au quatre point de l'armature du robot
		"""
        larg = self._dim[0]/2
        long = self._dim[1]/2

        x = self.posCenter[0]
        y = self.posCenter[1]

        TRC_V = Vecteur(+larg, -long)
        TLC_V = Vecteur(+larg, +long)
        BRC_V = Vecteur(-larg, -long)
        BLC_V = Vecteur(-larg, +long)
		
        if self.rotation!=0 :
            TRC_V.rotationAngle(self.rotation)
            TLC_V.rotationAngle(self.rotation)
            BRC_V.rotationAngle(self.rotation)
            BLC_V.rotationAngle(self.rotation)
		
        TRC_T = (TRC_V.x + x,TRC_V.y + y)
        TLC_T = (TLC_V.x + x,TLC_V.y + y)
        BRC_T = (BRC_V.x + x,BRC_V.y + y)
        BLC_T = (BLC_V.x + x,BLC_V.y + y)
		
        return [TRC_T,TLC_T,BLC_T,BRC_T]

    def getRectangle(self):
        """Permet d'obtenir les lignes représentant les 4 côtés du rectangle

			Returns:
				???
		"""
        coins = self.getCarcasse()

        haut = ((coins[1]),(coins[0]))
        bas = ((coins[2]),(coins[3]))
        gauche = ((coins[1]),(coins[3]))
        droit = ((coins[0]),(coins[3]))
        return [haut,bas,gauche,droit]