from simpack.Agent.robot import Robot as r
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
        self.last_update = 0

    
    def start(self):
        """
            Initialize la rotation déjà effectuée à 0
        """
        self.last_update = 0

    def step(self):
        """
            Met la vitesse des roues à une vitesse arbitraire de telle sorte a ce que la vitesse = 0 mais que la vitesse angulaire != 0.
            Incrémente parcouru par la valeur retournée par la fonction vitesse angulaire, fait tourner l'agent si stop() est false sinon ne return rien.
        """
        if self.last_update == 0:
            self.last_update = time.time()
            self.count = 0 
        else :
            #Calcul du temps entre le dernier appel et celui-ci
            time_passed = self.r.get_time_passed(self.last_update)
            self.last_update = time.time()

            print(f"ETAPE {self.count}")
            self.count += 1
            
            self.r.setVitesseRoue(-self.speed, self.speed)
            avancement = self.r.get_angle(time_passed)
            reste = self.angle - abs(self.r.angle_parcourue)
            
            print(f"Angle restant a parcourir {reste}")
            print(f"Angle parcouru {avancement}")

            if (abs(avancement) > reste) and (reste > 0) :
                self.speed = (reste/(180/math.pi))
                self.r.setVitesseRoue(-(self.speed)*0.5, self.speed*0.5)
        
    def stop(self):
        """
            Return True si self.parcouru > self.angle sinon return False
        """
        if abs(round(self.r.angle_parcourue,3)) >= self.angle:
            self.r.angle_parcourue = 0
            return True
        return False