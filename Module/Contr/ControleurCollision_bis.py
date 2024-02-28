from Module.Agent.Robot import Robot as rob
from Module.Env.Environnement import Environnement as env
from Module.Contr.VoirObstacle import VoirObstacle

class ControleurCollision():
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
        self.robot = robot
        self.env = en
        self.distance = 1
        self.speed = 0.7
        self.strats = [VoirObstacle(robot, en)]
        self.cur = -1
    
    def start(self):
        """
            Remet cur à -1 pour remettre le controleur sur la première instruction possible
        """
        self.cur = -1

    def step(self):
        """
            Fonction qui parcours les instructions 
        """
        if self.stop():
            return
        
        #Update de la distance en fonction de la distance calculer par rapport à l'obstacle
        self.distance = self.robot.capteur.distanceObstacle

        #Calcule de la dist pour le freinage par rapport à la longeur frontale du robot
        dist = self.distance - self.robot._dim[1]
        
        #Systeme de frein/decceleration
        if dist < 0 and self.distance != 0:
            new_speed = self.speed*abs(dist)/self.distance
            if self.speed > 0:
                self.speed -= round(new_speed, 5)
            else:
                self.speed = 0

        #Modification de la vitesse des roues puis avance selon la vitesse moyenne
        self.robot.setVitesseRoue(self.speed, self.speed)
        self.robot.avancerRobot()
        
        print("Distance entre le robot et le mur",self.robot.capteur.distanceObstacle)
        
        if self.cur<0 or self.strats[self.cur].stop():
            self.cur+=1
    
    def stop(self):
        """
            Condition d'arrêt de step
        """
        return self.cur >= len(self.strats)-1 and self.strats[self.cur].stop()