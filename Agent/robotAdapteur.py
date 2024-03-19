from Agent.robot import Robot
import math
from utils.vecteur import Vecteur

class robotFake:
    def __init__(self, x , y , vectD = Vecteur(0,-1)):
        self.MOTOR_LEFT = 0
        self.MOTOR_RIGHT = 0
        self.posCenter = (x,y)
        self.vectD = vectD
        self.rayon = 1
        self.rotation = self.vectD.calculerAngle(Vecteur(0,-1))

    def set_motor_dps(self, port, dps):
        print(f"Je met la vitesse de {port} à {dps}")
    
    def get_distance(self):
        pass

class robotAdapteur(Robot):

    def __init__(self, width, length, x = 0, y =0, vectD = Vecteur(0,-1)):
        self.rob = robotFake(x, y)
        super().__init__(width, length, x, y, vectD)

    def setVitesseRoue(self, d, g):
        self.rob.MOTOR_RIGHT = d
        self.rob.MOTOR_LEFT = g
        self.rob.set_motor_dps("MOTOR_LEFT", d)
        self.rob.set_motor_dps("MOTOR_RIGHT", g)
    
    def VitesseAngulaire(self) :
        """
			Permet de faire tourner le vecteur direction quand une roue va plus vite que l'autre.
		"""
        diff = self.rob.MOTOR_RIGHT - self.rob.MOTOR_LEFT
        angle = diff / self.rob.rayon
        pi = math.pi
        angle = angle * (180/pi)
        return round(angle,5)

    def avancerRobot(self):
        """
			Met à jour la position du robot en le faisant avancer en fonction de la vitesse et du vecteur direction
		"""
        vit = self.calcVitesseMoyenne()
        self.rob.posCenter = (round(self.rob.posCenter[0] + (self.rob.vectD.x * vit), 1),
						round(self.rob.posCenter[1] + (self.rob.vectD.y * vit), 1))
        print(f"J'ai une vitesse de {vit} et je suis à {self.rob.posCenter[0]} {self.rob.posCenter[1]}")

    def calcVitesseMoyenne(self) :
        """
            Calcule la vitesse moyenne du Robot en fonction de la vitesse des ses moteurs
        """
        return round((self.rob.MOTOR_LEFT + self.rob.MOTOR_RIGHT)/2,2)

    def rotateAllVect(self, angle) :
        """
			Rotation en degré du robot, ce qui demande une rotation du vecteur directeur et du vecteur representé par les 4 coins du robot
		"""
        self.rob.vectD.rotationAngle(angle)
        self.rotation += angle
    
    def update(self):
        self.rotateAllVect(self.VitesseAngulaire())
        self.avancerRobot()
        self.copie()

    def copie(self):
        self.posCenter = self.rob.posCenter
        self.vectD = self.rob.vectD