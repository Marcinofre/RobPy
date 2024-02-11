from Module.Env.Environnement import Environnement

class AvancerDroit():
    """
        Classe Strat de l'action d'avancer tout droit
    """
    def __init__(self, distance, env : Environnement):
        self.distance = distance
        self.env = env

    def start(self):
        self.parcouru = 0

    def step(self):
        self.parcouru += self.env.agent.vitesseMoyenne
        if self.stop() :
            return
        self.env.agent.avancerRobot()

    def stop(self):
        return self.parcouru > self.distance
    
    