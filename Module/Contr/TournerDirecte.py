from Module.Env.Environnement import Environnement

class TournerDirecte():
    """
        Classe Strat de l'action de tourner dans le sens directe
    """
    def __init__(self, angle: int, env : Environnement):
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
        self.env = env

    def updateTime(self) :
        """
            Permet d'obtenir l'update time de l'environnement
        """
        return self.env.clockPace
    
    def start(self):
        """
            Initialize la rotation déjà effectuée à 0
        """
        self.parcouru = 0

    def step(self):
        """
            Incrémente parcouru par [A compléter], fait tourner l'agent si stop() est false sinon ne return rien
        """
        self.parcouru += 5
        if self.stop() :
            return
        self.env.agent.rotateAllVect(5)
        print('je tourne')

    def stop(self):
        """
            Return True si self.parcouru > self.angle sinon return False
        """
        return self.parcouru > self.angle