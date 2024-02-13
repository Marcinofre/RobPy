from Module.Env.Environnement import Environnement


class AvancerDroit():
    """
        Classe Strat de l'action d'avancer tout droit
    """
    def __init__(self, distance: int, env : Environnement):
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
        self.env = env

    def updateTime(self) :
        """
            Permet d'obtenir l'update time de l'environnement
        """
        return self.env.clockPace
    
    def start(self):
        """
            Initialize la distance parcourue à 0
        """
        self.parcouru = 0

    def step(self):
        """
            Incrémente parcourue par la vitesseMoyenne de l'agent, fait avancer l'agent si stop() est false sinon ne return rien
        """

        self.env.agent.setVitesseRoue(0.2,0.2)
        self.parcouru += self.env.agent.vitesseMoyenne
        if self.stop() :
            return
        print('j\'avance')
        self.env.agent.avancerRobot()

    def stop(self):
        """
            Return True si self.parcouru > self.distance sinon return False
        """
        return self.parcouru > self.distance