from Module.Agent.Robot import Robot as rob
from Module.Env.Environnement import Environnement as env
from Module.Contr.AvancerDroit import AvancerDroit
from Module.Contr.TournerDirecte import TournerDirecte

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
        distance = 10
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
        self.isActive = False
    
    
    def start(self):
        """
            Remet cur à -1 pour remettre le controleur sur la première instruction possible
        """
        self.cur = -1
        print("VITESSE AU START : {self.speed}")
        for i in self.strats :
            i.speed = self.speed
            i.start()

    def step(self):
        """
            Fonction qui parcours les instructions 
        """
        print("STEP!")
        if self.stop():
            return
        if self.cur<0 or self.strats[self.cur].stop():
            self.robot.setVitesseRoue(0.5,0.5)
            self.cur+=1
    
    def stop(self):
        """
            Condition d'arrêt de step
        """
        return self.cur == len(self.strats)-1 and self.strats[self.cur].stop()