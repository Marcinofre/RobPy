from Module.Agent.Robot import Robot as rob
from Module.Env.Environnement import Environnement as env

class ControleurCollision():
    def __init__(self, r : rob, envi: env):
        """
           
        """
        self.r = r
        self.e = envi
        self.loin = False
        self.avancerVite = Avancer
        self.avancerLentement = Avancer

    def step(self):
        """
            
        """
        if self.stop():
            return
        if self.loin :
            self.avancerVite.step()
        else :
            self.avancerLentement.step()
        
    def stop(self):
        """
        
        """
        return self.e.doesCollide()
