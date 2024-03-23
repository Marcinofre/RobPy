from simpack.Agent.robot import Robot as rob
from simpack.Env.environnement import Environnement as env

class AvancerSansCollision():
    """
        Un controleur du robot dont le but est de lui faire tracer un carré
    """
    def __init__(self, robot: rob, en: env):
        """
            Constructeur de la classe ControleurCarré:
            arg env : Environnement que le controleur a accès
            
            ---

            Attributs d'instances :
            strats = Liste comprenant des instances des classes AvancerDroit et TournerDirecte, les instructions que le controleur enverra au Robot
            cur = Index permettant de désigner l'instruction qui est en train d'éxécuter (Initialisé à -1 et va jusqu'à len de strats -1)
        """
        self.env = en
        self.robot = robot                          # ---> Robot à controler
        self.distance = 0                           # ---> Distance à parcourir
        self.speed = 1                              # ---> Vitesse du robot initial
        self.pas_distance = 1                       # ---> Strategie courante
    
    def start(self):
        """
            Remet cur à -1 pour remettre le controleur sur la première instruction possible
        """
        self.pas_distance = 1
        self.robot.capteur.touchObstacle = False

    def step(self):
        """
            Fonction qui parcours les instructions 
        """

        if self.stop():
            return
        if self.env.retourCapteur(self.pas_distance):
            print(f"{self.robot.capteur.distanceObstacle} vs {self.robot.vectD.calcNorm()*max(self.robot._dim[0], self.robot._dim[1])*1.1}")
            if self.robot.capteur.distanceObstacle <= (self.robot.vectD.calcNorm()*max(self.robot._dim[0], self.robot._dim[1])/2)*1.1:
                self.speed = 0.0
        self.robot.setVitesseRoue(self.speed, self.speed)
        self.robot.capteur.touchObstacle = False
    
    def stop(self):
        """
            Condition d'arrêt de step
        """
        return self.speed == 0.0