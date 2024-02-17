from Module.Env.Environnement import Environnement
from Module.Contr.AvancerDroit import AvancerDroit
from Module.Contr.TournerDirecte import TournerDirecte

import time

class ControleurCarré():
    """
        Un controleur du robot dont le but est de lui faire tracer un carré
    """
    def __init__(self, env : Environnement):
        """
            Constructeur de la classe ControleurCarré:
            arg env : Environnement que le controleur a accès
            
            ---

            Attributs d'instances :
            strats = Liste comprenant des instances des classes AvancerDroit et TournerDirecte, les instructions que le controleur enverra au Robot
            cur = Index permettant de désigner l'instruction qui est en train d'éxécuter (Initialisé à -1 et va jusqu'à len de strats -1)
        """
        distance = 10
        self.strats = [AvancerDroit(distance, env), TournerDirecte(45, env), AvancerDroit(distance, env), TournerDirecte(45, env),AvancerDroit(distance, env), TournerDirecte(45, env),AvancerDroit(distance, env), TournerDirecte(45, env)]
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
        if self.cur<0 or self.strats[self.cur].stop():
            self.cur+=1
            self.useStrat(self.strats[self.cur])
    
    def stop(self):
        """
            Condition d'arrêt de step
        """
        return self.cur == len(self.strats)-1 and self.strats[self.cur].stop()
    
    def useStrat(self, strat):
        """
            Fonction permettant d'exécuter l'instruction désigné par step
        """
        strat.start()
        while not strat.stop():
            strat.step()
            time.sleep(1./strat.updateTime())

        print("Arrivé à destination ")
        self.step()
