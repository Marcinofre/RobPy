from Agent.robot import Robot as rob
from Env.environnement import Environnement as env
from Controleur.avancerSansCollision import AvancerSansCollision as asc
class ControleurCollision():
    """
        Un controleur du robot dont le but est de lui faire tracer un carré
    """
    def __init__(self, robot: rob, en : env):
        """
            Constructeur de la classe ControleurCarré:
            arg env : Environnement que le controleur a accès
            
            ---

            Attributs d'instances :
            strats = Liste comprenant des instances des classes AvancerDroit et TournerDirecte, les instructions que le controleur enverra au Robot
            cur = Index permettant de désigner l'instruction qui est en train d'éxécuter (Initialisé à -1 et va jusqu'à len de strats -1)
        """
        self.robot = robot
        self.speed = 1
        self.strats = [asc(robot, en)]
        self.cur = -1
    
    
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
        if self.cur<0 or self.strats[self.cur].stop():
            self.robot.setVitesseRoue(self.speed,self.speed)
            self.cur+=1
    
    def stop(self):
        """
            Condition d'arrêt de step
        """
        return self.cur == len(self.strats)-1 and self.strats[self.cur].stop()