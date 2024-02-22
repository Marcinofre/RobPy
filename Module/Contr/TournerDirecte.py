from Module.Env.Environnement import Environnement as env
from Module.Agent.Robot import Robot as r

class TournerDirecte():
    """
        Classe Strat de l'action de tourner dans le sens directe
    """
    def __init__(self, angle: int, rob : r, en : env):
        """
            Constructeur de la classe TournerDirecte:
            arg env : Environnement que le controleur a accès
            angle : Angle en degré par lequel l'agent doit être tourné par la classe TournerDirecte

            ---

            Attributs d'instance:
            angle      -> Angle en degré par lequel l'agent doit être tourné par la classe TournerDirecte
            env        -> Environnement dans lequel on tourne un agent
            parcouru   -> Rotation déjà effectué par la classe TournerDirecte
        """
        self.angle = angle
        self.r = rob
        self.e = en
    
    def start(self):
        """
            Initialize la rotation déjà effectuée à 0
        """
        self.parcouru = 0

    def step(self):
        """
            Met la vitesse des roues à une vitesse arbitraire de telle sorte a ce que la vitesse = 0 mais que la vitesse angulaire != 0.
            Incrémente parcouru par la valeur retournée par la fonction vitesse angulaire, fait tourner l'agent si stop() est false sinon ne return rien.
        """
        self.r.setVitesseRoue(-0.043633, 0.043633)
        avancement = self.r.VitesseAngulaire()
        print(f"{avancement}")
        self.parcouru -= avancement
        if self.stop() :
            return
        self.r.rotateAllVect(avancement)
        print('je tourne')

    def stop(self):
        """
            Return True si self.parcouru > self.angle sinon return False
        """
        return self.parcouru > self.angle