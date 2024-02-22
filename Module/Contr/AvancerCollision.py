from Module.Agent.Robot import Robot as rob
from Module.Env.Environnement import Environnement as env

class AvancerCollision():
    def __init__(self, distance: int, r : rob, envi: env):
        """
            Constructeur de la classe AvancerDroit:
            arg env : Environnement que le controleur a accès
            distance : Distance à parcourir dans la classe AvancerCollision

            ---

            Attributs d'instance:
            distance   -> Distance à parcourir par la classe AvancerCollision
            env        -> Environnement dans lequel on bouge un agent
            parcouru   -> Distance parcouru jusqu'à maintenant par la classe AvancerCollision
        """
        self.distance = distance
        self.r = r
        self.e = envi