from simpack.Agent.robot import Robot as rob
from simpack.Controleur.avancerDroit import AvancerDroit
from simpack.Controleur.tournerDirecte import TournerDirecte
import time

class controleurgenerale:
    def __init__(self,Robot:rob) -> None:
        self.robot=Robot

    def parcourir_carre(self, cote):
        for _ in range(4):  
            avancer = AvancerDroit(distance=cote, speed=self.robot.speed, r=self.robot)
            avancer.start()
            while not avancer.stop():
                avancer.step()
                time.sleep(0.01)

            tourner = TournerDirecte(angle=90, rob=self.robot)
            tourner.start()
            while not tourner.stop():
                tourner.step()
                time.sleep(0.01) 

    def collision():
        pass