from Agent.robot import Robot

class RobotFake:
    def __init__(self):
        self.leftmot = 0
        self.rightmot = 0

    def set_motor_dps(self, port, dps):
        if port == "G":
            self.leftmot = dps
        if port == "D":
            self.rightmot = dps
class robotAdapteur(Robot):

    def __init__(self):
        self.rob = RobotFake()
    
    def setVitesseRoue(self, d, g):
        self.rob.set_motor_dps("D", d)
        self.rob.set_motor_dps("G", g)