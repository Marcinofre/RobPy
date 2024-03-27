from simpack.Agent.robot import Robot as r
from simpack.utils.vecteur import Vecteur
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
        self.pas_angle = 1
        self.initial_speed = self.speed 

    
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

            #Création du vecteur d'arrivée en fonction de la postion de départ et d'un angle
            self.vecteur_finale = Vecteur(self.r.vectD.x, self.r.vectD.y)

            # -self.angle car il tourne a gauche, si on laisse self.angle il fera trois quart de tour pour aller a droite
            self.vecteur_finale.rotationAngle(-self.angle)
            
            # Compteur d'etape step effectuer
            self.count = 0 
            self.speed = self.initial_speed
        else :
            #Calcul du temps entre le dernier appel et celui-ci
            time_passed = self.r.get_time_passed(self.last_update)
            self.last_update = time.time()

            print(f"ETAPE {self.count}")
            self.count += 1
            
            self.r.setVitesseRoue(-self.speed, self.speed)

            # On calcul l'angle qui sépart le vecteur finale de la position du vecteur courant
            angle_restant = self.vecteur_finale.calculerAngle(self.r.vectD)
            self.pas_angle = self.r.VitesseAngulaire()*time_passed
            print(f"Angle restant a parcourir : {angle_restant}")
            print(f"Pas de l'angle : {self.pas_angle}")


            if abs(self.pas_angle) > angle_restant :
                self.speed /= 2
                self.r.setVitesseRoue(-self.speed, self.speed)

            
        
    def stop(self):
        """
            Return True si self.parcouru > self.angle sinon return False
        """
        return self.vecteur_finale.calculerAngle(self.r.vectD) == 0