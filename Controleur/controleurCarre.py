from Agent.robot import Robot as rob
from Controleur.avancerDroit import AvancerDroit
from Controleur.tournerDirecte import TournerDirecte
import time

class ControleurCarre():
    """
        Un controleur du robot dont le but est de lui faire tracer un carré
    """
    def __init__(self, robot: rob):
        """
            Constructeur de la classe ControleurCarré:
            arg env : Environnement que le controleur a accès
            
            ---

            Attributs d'instances :
            strats = Liste comprenant des instances des classes AvancerDroit et TournerDirecte, les instructions que le controleur enverra au Robot
            cur = Index permettant de désigner l'instruction qui est en train d'éxécuter (Initialisé à -1 et va jusqu'à len de strats -1)
        """
        distance = 5
        self.robot = robot
        self.speed = 1
        self.strats = [AvancerDroit(distance, self.speed,  robot), 
                       TournerDirecte(90, robot), 
                       AvancerDroit(distance, self.speed, robot), 
                       TournerDirecte(90, robot), 
                       AvancerDroit(distance, self.speed, robot), 
                       TournerDirecte(90, robot),
                       AvancerDroit(distance, self.speed, robot), 
                       TournerDirecte(90, robot)]
        self.cur = -1
        self.last_update = 0
    
    
    def start(self):
        """
            Remet cur à -1 pour remettre le controleur sur la première instruction possible
        """
        self.cur = -1
        for i in self.strats :
            i.speed = self.speed
            i.start()

    def step(self):
        """
            Fonction qui parcours les instructions 
        """ 

        if self.stop():
            return
        if self.cur < 0 or self.strats[self.cur].stop():
            self.robot.setVitesseRoue(0,0)
            self.last_update = time.time()
            self.cur+=1
        else:
            print(f"time passed : {time.time()-self.last_update}")
        
            
    
    def stop(self):
        """
            Condition d'arrêt de step
        """
        return self.cur == len(self.strats)-1 and self.strats[self.cur].stop()