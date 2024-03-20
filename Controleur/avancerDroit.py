import time
from Agent.robot import Robot


class AvancerDroit():
    """
        Classe Strat de l'action d'avancer tout droit
    """
    def __init__(self, distance: int, speed, r : Robot):
        """
            Constructeur de la classe AvancerDroit
            
            Args:
                distance: Distance à parcourir
                speed: Vitesse initiale
                r: Robot sur lequel s'applique la stratégie

            Attributes:
                distance: Distance à parcourir
                speed: Vitesse en cours à appliquer au robot
                parcouru: Distance parcouru jusqu'à maintenant par la classe AvancerDroit
                r: Robot sur lequel s'applique la stratégie
                last_update: Temps de la dernière mise a jour de de l'appel de step()
                
        """
        self.distance = distance
        self.speed = speed
        self.r = r
        self.parcouru = 0
        self.last_update = 0 
    
    def start(self):
        """
            Initialize la distance parcourue à 0 et du temps
        """
        #Initialisation de la distance parcourue
        self.parcouru = 0

    def step(self):
        """
            Applique la stratégie:
                - Calcule le temps passée entre les deux appels de step
                - Calcule la distance parcourues selon la vitesse du robot actuelle et les temps passée
                - Ajoute la distance parourue à self.parouru
        """
        
        if self.last_update == 0:
            self.last_update = time.time()
        else :
            self.r.setVitesseRoue(self.speed,self.speed)
            current_time = time.time()
            time_passed = current_time - self.last_update
            self.last_update = current_time
            #Distance parcourue selon le temps passer et la vitesse actuelle
            distance_traveled = self.r.get_distance_parcourue(time_passed)
            if distance_traveled > self.distance - self.parcouru > 0 :
                self.speed = (self.distance - self.parcouru)/time_passed
                self.r.setVitesseRoue(self.speed, self.speed)
                distance_traveled = self.r.get_distance_parcourue(time_passed)
            #Mise a jour de la distance parcourue en fonction du temps passé
            self.parcouru += distance_traveled
        
        

    def stop(self):
        """
            Return True si self.parcouru > self.distance sinon return False
        """
        if round(self.parcouru,1) >= self.distance:
            self.parcouru = 0
            self.last_update = 0
            return True
        return False