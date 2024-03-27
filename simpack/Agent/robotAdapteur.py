from simpack.Agent.robot import Robot
from simpack.Agent.robot import Capteur
from simpack.utils.vecteur import Vecteur
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
        self.vectD = Vecteur(0,-1)
        self.initial_vectD = self.vectD
        self.rotation = self.vectD.calculerAngle(Vecteur(0,-1))
        self.last_update = time.time()
        self._dim = (30,45)
        self.rayon = self._dim[0]/2
        self.capteur = self.capteur = Capteur(self.vectD)
        self.isControlled = False
        self.distance_parcourue = 0
        self.angle_parcourue = 0

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
        self.distance_parcourue += self.calcVitesseMoyenne() * deltat
        return self.calcVitesseMoyenne() * deltat

    def get_time_passed(self, t):
        time_passed =  t -self.last_update
        return abs(time_passed)
    
    def get_angle(self, deltat):
        self.angle_parcourue += self.vitesseAngulaire() * deltat
        return self.vitesseAngulaire() * deltat
    
    def vitesseAngulaire(self) -> float:
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
        self.vectD = Vecteur(self.initial_vectD.x, self.initial_vectD.y)
        self.capteur.ray = Vecteur(self.capteur.initial_ray.x, self.capteur.initial_ray.y)
        self.rotation += angle
        self.capteur.ray.rotationAngle(self.rotation)
        self.vectD.rotationAngle(self.rotation)
        if angle > 0:
            print(f"{self.vectD.x} {self.vectD.y}")
    
    def update(self, deltat):
        """
            Mise à jour du vecteur directeur et la position du robot
        """
        deltat = self.get_time_passed(time.time())
        self.rotateAllVect(self.vitesseAngulaire()*deltat)
        self.avancerRobot(deltat)
        self.last_update = time.time()