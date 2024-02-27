from Module.Agent.Robot import Robot as rob
from Module.Env.Environnement import Environnement as env


class VoirObstacle():
    """
        Classe Strat de l'action d'avancer tout droit
    """
    def __init__(self, r : rob, envi: env):
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
        self.r = r
        self.e = envi
        self.distance_vue = 0
        self.pas_distance = 1
    
    def start(self):
        """
            Initialize la distance parcourue à 0
        """
        self.r .capteur.touchObstacle = False
        self.distance_vue = 0

    def step(self):
        """
            Incrémente parcourue par la vitesseMoyenne de l'agent, fait avancer l'agent si stop() est false sinon ne return rien
        """
        
        if self.stop() :
            print(f"Stopped by obstacle ? : {self.r.capteur.touchObstacle}")
            print(f"Stopped by vision_max ? : {self.r.capteur.vision < self.distance_vue}")	
            return
        self.e.retourCapteur(self.pas_distance)
        

    def stop(self):
        """
            Return True si un obstacle à été détecté ou que la limite du capteur à été atteinte sinon return False
        """
        
        return self.r.capteur.touchObstacle or self.r.capteur.vision < self.distance_vue