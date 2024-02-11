from Module.Env.Environnement import Environnement
from Module.Contr.AvancerDroit import AvancerDroit
from Module.Contr.TournerDroite import TournerDroite

import time

class ControleurCarré():
    def __init__(self, env : Environnement):
        distance = 10
        self.strats = [AvancerDroit(distance, self.env), TournerDroite(90, self.env), AvancerDroit(distance, self.env), TournerDroite(90, self.env),AvancerDroit(distance, self.env), TournerDroite(90, self.env),AvancerDroit(distance, self.env), TournerDroite(90, self.env)]
        self.env = env
        self.cur = -1
    
    def start(self):
        self.cur = -1

    def step(self):
        if self.stop():
            return
        if self.cur<0 or self.strats[self.cur].stop():
            self.cur+=1
            self.strats[self.cur].step()
    
    def stop(self):
        return self.curr ==len(self.strats)-1 and self.strats[self.cur].stop()
    
    def avancer_robot(self,distance):
        strategie=AvancerDroit(distance,self.env)
        strategie.start()

        while not strategie.stop():
            strategie.step()
            time.sleep(1./strategie.updateTime())

        print("Arrivé à destination ")
