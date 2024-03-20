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

    def step(self):
        """
            Met la vitesse des roues à une vitesse arbitraire de telle sorte a ce que la vitesse = 0 mais que la vitesse angulaire != 0.
            Incrémente parcouru par la valeur retournée par la fonction vitesse angulaire, fait tourner l'agent si stop() est false sinon ne return rien.
        """
        if self.last_update == 0:
            self.last_update = time.time()
        else :
            self.r.setVitesseRoue(-self.speed, self.speed)
            #Calcul du temps entre le dernier appel et celui-ci
            current_time = time.time()
            time_passed = current_time - self.last_update 
            self.last_update = current_time
            
            avancement = self.r.VitesseAngulaire()
            if abs(avancement)*time_passed > (self.angle - self.parcouru) > 0 :
                print("AVANCEMENT TROP HAUT")
                self.speed = ((self.angle-self.parcouru)*self.r.rayon)/(180/math.pi)
                self.r.setVitesseRoue(-(self.speed)/2, self.speed/2)
                print(f"{self.speed}")
                avancement = self.r.VitesseAngulaire() * time_passed
            self.parcouru += abs(avancement*time_passed)
            print(abs(avancement))
        
    def stop(self):
        """
            Return True si self.parcouru > self.angle sinon return False
        """
        if round(self.parcouru,3) >= self.angle:
            self.parcouru = 0
            self.last_update = 0
            return True
        return False