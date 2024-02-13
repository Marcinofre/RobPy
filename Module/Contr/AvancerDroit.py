from Module.Env.Environnement import Environnement


class AvancerDroit():
    """
        Classe Strat de l'action d'avancer tout droit
    """
    def __init__(self, distance, env : Environnement):
        """
            Constructeur de la classe AvancerDroit:
            arg env : Environnement que le controleur a accès
            
            ---

            Attributs d'instance:
            distance   -> Distance à parcourir par la classe AvancerDroit
            env        -> Environnement dans lequel on bouge un agent
        """
        self.distance = distance
        self.env = env

    def updateTime(self) :
        """
            Permet d'obtenir l'update time de l'environnement
        """
        return self.env.clockPace
    
    def start(self):
        """
            Remet la distance parcourue à 0
        """
        self.parcouru = 0

    def step(self):
        """
            Incrémente parcourue par la vitesseMoyenne de l'agent, fait avancer l'agent si stop() est false sinon ne return rien
        """
        self.parcouru += self.env.agent.vitesseMoyenne
        if self.stop() :
            return
        self.env.agent.avancerRobot()

    def stop(self):
        """
            Return True si self.parcouru > self.distance sinon return False
        """
        return self.parcouru > self.distance