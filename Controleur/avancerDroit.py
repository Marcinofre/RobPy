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

        #initialisation du temps
        self.last_update = time.time()

    def step(self):
        """
            Applique la stratégie:
                - Calcule le temps passée entre les deux appels de step
                - Calcule la distance parcourues selon la vitesse du robot actuelle et les temps passée
                - Ajoute la distance parourue à self.parouru
        """
        
        if self.stop() :
            return
        
        self.r.setVitesseRoue(self.speed,self.speed)
        
        #Calcul du temps entre le dernier appel et celui-ci
        current_time = time.time()
        time_passed = current_time - self.last_update
        self.last_update = current_time

        #Distance parcourue selon le temps passer et la vitesse actuelle
        distance_traveled = self.speed * time_passed
        
        #Mise a jour de la distance parcourue en fonction du temps passé
        self.parcouru += distance_traveled

        
        avancement = self.r.calcVitesseMoyenne()
        
        if avancement> self.distance - self.parcouru > 0 :
            self.speed = self.distance - self.parcouru
            self.r.setVitesseRoue(self.speed, self.speed)
            avancement = self.r.calcVitesseMoyenne()
        
        self.parcouru += avancement
        
        

    def stop(self):
        """
            Return True si self.parcouru > self.distance sinon return False
        """
        return self.parcouru >= self.distance