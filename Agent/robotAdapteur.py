from Agent.robot import Robot
import math
from utils.vecteur import Vecteur
import time

class robotFake:
    """
        Représentation factice du Robot irl et de ses fonctions
    """
    def __init__(self, x: int, y: int, vectD = Vecteur(0,-1)) -> None:
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

        self.MOTOR_LEFT = 0
        self.MOTOR_RIGHT = 0
        self.posCenter = (x,y)
        self.vectD = vectD
        self.rayon = 1
        self.rotation = self.vectD.calculerAngle(Vecteur(0,-1))

    def set_motor_dps(self, port, dps) -> None:
        """
            Définit la vitesse `dps` d'un moteur choisit selon le `port`
            
            Args:

                port: Port sur lequel on communique
                dps: Vitesse de rotation du moteur
        """
        #print(f"Je met la vitesse de {port} à {dps}")
    
    def get_distance(self) -> None:
        pass

class robotAdapteur(Robot):
    """
        Classe permettant de communiquer avec un autre robot que le robot simulé. Plus précisément, cet adaptateur permet de communiquer avec le robot IRL
    """

    def __init__(self, width:int, length:int, x:int = 0, y:int = 0, vectD = Vecteur(0,-1)):
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
        
        self.rob = robotFake(x, y)
        super().__init__(width, length, x, y, vectD)

    def setVitesseRoue(self, d:"int | float", g:"int | float"):
        """
            Définit les vitesses des moteurs

            Args:
                d: Vitesse du moteur droit
                g: Vitesse du moteur gauche
        """
        self.rob.MOTOR_RIGHT = d
        self.rob.MOTOR_LEFT = g
        self.rob.set_motor_dps("MOTOR_LEFT", d)
        self.rob.set_motor_dps("MOTOR_RIGHT", g)
    
    def VitesseAngulaire(self) -> float:
        """
			Permet de faire tourner le vecteur direction quand une roue va plus vite que l'autre.

            Returns:
                Renvoie l'angle de rotation induit par la vitesse des roue en degré (arrondie au 5eme chiffre significatif)
		"""
        diff = self.rob.MOTOR_RIGHT - self.rob.MOTOR_LEFT
        angle = diff / self.rob.rayon
        angle = angle * (180/math.pi)
        return round(angle,5)

    def avancerRobot(self, deltat) -> None:
        """
			Met à jour la position du robot en le faisant avancer en fonction de la vitesse et du vecteur direction
		"""
        vit = self.calcVitesseMoyenne()
        self.rob.posCenter = (  round(self.rob.posCenter[0] + (self.rob.vectD.x * vit*deltat), 1),
						        round(self.rob.posCenter[1] + (self.rob.vectD.y * vit*deltat), 1))
        print(f"J'ai une vitesse de {vit} et je suis à {self.rob.posCenter[0]} {self.rob.posCenter[1]}")

    def calcVitesseMoyenne(self) :
        """
            Calcule la vitesse moyenne du Robot en fonction de la vitesse des ses moteurs
        """
        return round((self.rob.MOTOR_LEFT + self.rob.MOTOR_RIGHT)/2,2)

    def rotateAllVect(self, angle:float) :
        """
			Rotation en degré du vecteur directeur et du vecteur unitaire du capteur du robot

            Args:

                angle: Angle de rotation à appliquer en degré
		"""
        self.rob.vectD.rotationAngle(angle)
        self.rotation += angle
    
    def update(self, deltat):
        """
            Mise à jour du vecteur directeur et la position du robot
        """
        self.rotateAllVect(self.VitesseAngulaire()*deltat)
        self.avancerRobot(deltat)
        self.update_trace()
        self.copie()
        self.last_update = time.time()

    def copie(self):
        """
            Copie les positions et le vecteur directeur du robot simuler au robot irl ???
        """
        self.posCenter = self.rob.posCenter
        self.vectD = self.rob.vectD