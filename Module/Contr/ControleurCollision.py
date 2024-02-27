from Module.Agent.Robot import Robot as rob
from Module.Env.Environnement import Environnement as env

class ControleurCollision():
    def __init__(self, r : rob, envi: env):
        """
            Constructeur de la classe ControleurCarré:
            arg envi : Environnement que le controleur a accès
            arg r : Robot que le controleur manipule

            ---

            Attributs d'instances :
            loin = Booléen disant si le robot est à plus d'une distance (arbitrairement choisit) d'un obstacle
        """
        self.r = r
        self.e = envi
        self.loin = None

    def start(self):
        """
            Initialize le booléen loin
        """
        if self.r.capteur.RayTouchObsctacle() > 100 :
            self.loin = True
        else:
            self.loin = False

    def step(self):
        """
            Fonction ayant 3 possibilités :
            - stop() est true donc le robot s'arrête
            - self.loin est true, on met les vitesses des roues à 1,1 et on avance
            - self.loin est false, on met la distance en pourcentage et multiplie la vitesse 1,1 des roues par ce pourcentage, la vitesse va donc tendre vers 0
        """
        if self.stop():
            return
        if self.loin :
            self.r.setVitesseRoue(1,1)
            self.r.avancerRobot()
        else :
            distance = 0.01*self.r.capteur.RayTouchObsctacle()
            self.r.setVitesseRoue(1*distance,1*distance)
            self.r.avancerRobot()
        
    def stop(self):
        """
            Condition d'arrêt de step, doesCollide() renverra True or False dépendemment de si le robot risque d'entrer en collision avec un objet
        """
        return self.e.doesCollide()
