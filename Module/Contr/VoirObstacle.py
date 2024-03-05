from Module.Agent.Robot import Robot as robot
from Module.Env.Environnement import Environnement as env


class VoirObstacle():
    """
        Classe Strat de l'action d'avancer tout droit
    """
    def __init__(self, robot : robot, env: env):
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
        self.robot = robot
        self.env = env
        self.distance_vue = 0
        self.pas_distance = 1
    
    def start(self):
        """
            Initialise la distance parcourue à 0
        """
        self.robot.capteur.touchObstacle = False
        self.distance_vue = 0

    def step(self):
        """
            Incrémente parcourue par la vitesseMoyenne de l'agent, fait avancer l'agent si stop() est false sinon ne return rien
        """
        if self.env.retourCapteur(self.pas_distance):
            print(f"Stopped by obstacle ? : {self.robot.capteur.touchObstacle}")
            print(f"Stopped by vision_max ? : {self.robot.capteur.vision < self.distance_vue}")	
            return

    def stop(self):
        """
            Return True si un obstacle à été détecté ou que la limite du capteur à été atteinte sinon return False
        """
        
        return self.robot.capteur.touchObstacle or self.robot.capteur.vision < self.distance_vue