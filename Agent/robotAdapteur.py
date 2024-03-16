from Agent.robot import Robot
import time
class RobotFake:
    def __init__(self, x = 0, y = 0, vectD = (0,-1)):
        self.leftmot = 0
        self.rightmot = 0
        self.posCenter = (x,y)
        self.vectD = vectD

    def set_motor_dps(self, port, dps):
        if port == "G":
            self.leftmot = dps
        if port == "D":
            self.rightmot = dps
    
    def vitesseMoyenne(self):
        return (self.leftmot+self.rightmot)/2
    
    def avancerRobot(self):
        vit = self.vitesseMoyenne()
        self.posCenter = (self.posCenter[0]+vit*self.vectD[0], self.posCenter[1]+vit*self.vectD[1])
        print(f"J'ai une vitesse de {vit} et je suis à {self.posCenter[0]} {self.posCenter[1]}")

class robotAdapteur(Robot):

    def __init__(self):
        self.rob = RobotFake()
    
    def setVitesseRoue(self, d, g):
        self.rob.set_motor_dps("D", d)
        self.rob.set_motor_dps("G", g)

    def update(self):
        self.rob.avancerRobot()