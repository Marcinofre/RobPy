from Module.Agent.Robot import Robot as rob
from Module.Env.Environnement import Environnement as env
from Module.Contr.VoirObstacle import VoirObstacle

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
        self.speed = 0.6                            # ---> Vitesse du robot initial
        self.strats = [VoirObstacle(robot, en)]
        self.cur = -1 
        self.pas_distance = 1                              # ---> Strategie courante
    
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

        #if self.stop():
            #return
        #self.distance = self.robot.capteur.distanceObstacle
        #if self.distance <100:
            #if self.speed != 0:
               # self.speed = round(self.speed * self.distance*0.01, 2)  # On applique le freinage à la roue en évitant les valeures absurdes
        #self.robot.setVitesseRoue(self.speed, self.speed) 
        if self.env.retourCapteur(self.pas_distance):
            print("Where i Am")
            if self.robot.capteur.distanceObstacle < 45 :
                print("-----------------------------------------Where i Am---------------------------------------------------------")
                self.speed = 0.0
                self.robot.setVitesseRoue(self.speed, self.speed)
        
            
        print(" Distance entre le robot et l'obstacle ",self.robot.capteur.distanceObstacle)
        
        if self.cur<0 or self.strats[self.cur].stop():
            self.cur+=1
    
    def stop(self):
        """
            Condition d'arrêt de step
        """
        return self.cur >= len(self.strats)-1 and self.strats[self.cur].stop()