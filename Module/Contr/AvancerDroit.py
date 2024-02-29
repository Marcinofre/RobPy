from Module.Agent.Robot import Robot as rob
from Module.Env.Environnement import Environnement as env


class AvancerDroit():
    """
        Classe Strat de l'action d'avancer tout droit
    """
    def __init__(self, distance: int, speed, r : rob):
        """
            Constructeur de la classe AvancerDroit:
            arg env : Environnement que le controleur a accès
            distance : Distance à parcourir dans la classe AvancerDroit

            ---

            Attributs d'instance:
            distance   -> Distance à parcourir par la classe AvancerDroit
            env        -> Environnement dans lequel on bouge un agent
            parcouru   -> Distance parcouru jusqu'à maintenant par la classe AvancerDroit
        """
        self.distance = distance
        self.speed = speed
        self.r = r
        self.parcouru = 0
    
    def start(self):
        """
            Initialize la distance parcourue à 0
        """
        self.parcouru = 0

    def step(self):
        """
            Incrémente parcourue par la vitesseMoyenne de l'agent, fait avancer l'agent si stop() est false sinon ne return rien
        """

        self.r.setVitesseRoue(self.speed,self.speed)
        self.parcouru += self.r.vitesseMoyenne
        if self.stop() :
            return

    def stop(self):
        """
            Return True si self.parcouru > self.distance sinon return False
        """
        return self.parcouru > self.distance