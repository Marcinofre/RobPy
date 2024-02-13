from Module.Env.Environnement import Environnement

class TournerDirecte():
    """
        Classe Strat de l'action de tourner dans le sens directe
    """
    def __init__(self, angle, env : Environnement):
        self.angle = angle
        self.env = env

    def updateTime(self) :
        return self.env.clockPace
    
    def start(self):
        self.parcouru = 0

    def step(self):
        self.parcouru += 5
        if self.stop() :
            return
        self.env.agent.rotateAllVect(5)

    def stop(self):
        return self.parcouru > self.angle