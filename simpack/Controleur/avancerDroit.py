import time
from simpack.Agent.robot import Robot


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
        self.last_update = 0 
    
    def start(self):
        """
            Initialize la distance parcourue à 0 et du temps
        """
        #Initialisation de la distance parcourue
        self.last_update = 0

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
            time_passed = self.r.get_time_passed(self.last_update)
            self.last_update = time.time()
            #Distance parcourue selon le temps passer et la vitesse actuelle
            distance_traveled = self.r.get_distance_parcourue(time_passed)
            reste = self.distance - self.r.distance_parcourue
            if distance_traveled > reste > 0 :
                self.speed = round((reste)/time_passed, 0)
                self.r.setVitesseRoue(self.speed, self.speed)
        
        

    def stop(self):
        """
            Return True si self.parcouru > self.distance sinon return False
        """
        if round(self.r.distance_parcourue,1) >= self.distance:
            self.r.distance_parcourue = 0
            return True
        return False