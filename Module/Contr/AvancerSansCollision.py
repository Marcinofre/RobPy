from Module.Agent.Robot import Robot as rob
from Module.Env.Environnement import Environnement as env
from Module.Contr.VoirObstacle import VoirObstacle
from Module.Agent.Capteur import Capteur

class AvancerSansCollision():
    """
        Un controleur du robot 
    """
    def __init__(self, robot: rob, en: env):
        """
            Constructeur de la classe AvancerSansCollision :
            arg env : Environnement que le controleur a accès
            
            ---

            Attributs d'instances :
            strats = Liste comprenant des instances des classes AvancerDroit et TournerDirecte, les instructions que le controleur enverra au Robot
            cur = Index permettant de désigner l'instruction qui est en train d'éxécuter (Initialisé à -1 et va jusqu'à len de strats -1)
        """
        self.robot = robot                          # ---> Robot à controler
        self.distance = 0                           # ---> Distance à parcourir
        self.speed = 0.6                            # ---> Vitesse du robot initial
        self.strats = [VoirObstacle(robot, en)]
        self.cur = -1                               # ---> Strategie courante
        self.isActive = False
    
    def start(self):
        """
            Remet cur à -1 pour remettre le controleur sur la première instruction possible
        """
        self.cur = -1
        for i in self.strats :
            i.start()

    def step(self):
        """
            Fonction qui parcours les instructions 
        """

        if self.stop():
            return
        
        self.distance = self.robot.capteur.getObstacle() # On update la distance entre le robot et l'obstacle
        self.freinage = - ( self.speed ** 2 ) / ( 2 * self.distance) # On calcule le freinage nécéssaire 
        self.speed -= round(self.freinage, 2)  # On applique le freinage à la roue en évitant les valeures absurdes
        self.robot.setVitesseRoue(self.speed, self.speed)  # Modification de la vitesse des roues puis avance selon la vitesse moyenne
        
        print("Distance entre le robot et le mur",self.robot.capteur.distanceObstacle)
        
        if self.cur<0 or self.strats[self.cur].stop():
            self.cur+=1
    
    def stop(self):
        """
            Condition d'arrêt de step
        """
        return self.cur >= len(self.strats)-1 and self.strats[self.cur].stop()