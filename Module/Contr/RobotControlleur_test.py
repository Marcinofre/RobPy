from Module.Env.Environnement import Environnement
from Module.Agent.Robot import Robot
from AvancerDroit import AvancerDroit

import time

class RobotControlleur():
    def __init__(self,Agent : Robot, env : Environnement):
        self.Robot=Agent
        self.env=env
    

    def avancer_robot(self,distance):
        strategie=AvancerDroit(distance,self.env)
        strategie.start()

        while not strategie.stop():
            strategie.step()
            time.sleep(1./strategie.updateTime())

        print("Arrivé à destination ")
