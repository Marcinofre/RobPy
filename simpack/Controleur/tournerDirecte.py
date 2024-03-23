from Agent.robot import Robot as r
import time
import math


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
        self.last_update = 0

    def step(self):
        """
            Met la vitesse des roues à une vitesse arbitraire de telle sorte a ce que la vitesse = 0 mais que la vitesse angulaire != 0.
            Incrémente parcouru par la valeur retournée par la fonction vitesse angulaire, fait tourner l'agent si stop() est false sinon ne return rien.
        """
        if self.last_update == 0:
            self.last_update = time.time()
        else :
            #Calcul du temps entre le dernier appel et celui-ci
            current_time = time.time()
            time_passed = current_time - self.last_update 
            self.last_update = current_time
            
            self.r.setVitesseRoue(-self.speed, self.speed)
            avancement = self.r.VitesseAngulaire()
            if abs(avancement)*time_passed > (self.angle - self.parcouru) > 0 :
                self.speed = ((self.angle-self.parcouru)*self.r.rayon)/(180/math.pi)
                self.r.setVitesseRoue(-(self.speed)/2, self.speed/2)
                avancement = self.r.VitesseAngulaire() * time_passed
            self.parcouru += abs(avancement*time_passed)
        
    def stop(self):
        """
            Return True si self.parcouru > self.angle sinon return False
        """
        return round(self.parcouru,3) >= self.angle