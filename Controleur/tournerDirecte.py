from Agent.robot import Robot as r
import time


class TournerDirecte():
    """
        Classe Strat de l'action de tourner dans le sens directe
    """
    def __init__(self, angle: int, rob : r):
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
        self.speed = 1
        self.parcouru = 0
        self.last_update = 0

    
    def start(self):
        """
            Initialize la rotation déjà effectuée à 0
        """
        self.parcouru = 0
        self.last_update = time.time()

    def step(self):
        """
            Met la vitesse des roues à une vitesse arbitraire de telle sorte a ce que la vitesse = 0 mais que la vitesse angulaire != 0.
            Incrémente parcouru par la valeur retournée par la fonction vitesse angulaire, fait tourner l'agent si stop() est false sinon ne return rien.
        """
        if self.stop() :
            return
        
        #Calcul du temps entre le dernier appel et celui-ci
        current_time = time.time()
        time_passed = current_time - self.last_update
        self.last_update = current_time
        
        self.r.setVitesseRoue(-self.speed, self.speed)
        avancement = self.r.VitesseAngulaire()
        
        while abs(avancement) > self.angle - self.parcouru > 0 :
            self.speed -= self.speed*0.1
            self.r.setVitesseRoue(-self.speed, self.speed)
            avancement = self.r.VitesseAngulaire()
        
        self.parcouru += abs(avancement)
        
    def stop(self):
        """
            Return True si self.parcouru > self.angle sinon return False
        """
        return round(self.parcouru,4) >= self.angle