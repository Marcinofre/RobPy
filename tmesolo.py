from Env.environnement import Environnement as env
from Env.environnement import Obstacle
from Agent.robot import Robot
from utils.interface import Interface
from Controleur.controleurCarre import ControleurCarre
from Controleur.controleurCollision import ControleurCollision
from Agent.robotAdapteur import robotAdapteur
from Controleur.tournerDirecte import TournerDirecte
from utils.vecteur import Vecteur
import time
import threading


def introductionSimulation():
    """
        Affiche une introduction et retourne un bool selon si la simulation doit etre demarrer avec ou sans interface graphique depuis le terminal
    """
    print("The RobPy simulation is currently being initialized.")
    print("Please kindly follow the instructions that may follow")
    print("For each instruction, please write \"yes\" or (\"y\") or \"no\" (\"n\"). If another element is detected, it will be considered \"no\" as default")
    response = input("Do you want to start the simulation with the interface ?\n--->>>")

    return response in ["yes", "y"]

def updateEnv(env):
    """
        Update l'ensemble des classe de la simulation
    """
    env.initSimulation()
    while env.isRunning :
        env.update()			        #---> Update l'environnement
        time.sleep(1./env.clockPace)	#---> frame par sec 

def updateContr(env, contr):
    if env.agent.isControlled:
        while env.isRunning:
            if not env.agent.isControlled :
                env.agent.setVitesseRoue(0,0)
                env.agent.capteur.ray = env.agent.capteur.treatVector(env.agent.vectD)
                env.agent.capteur.interfaceRay = env.agent.capteur.ray
                updateContr(env, contr)
                break
            if contr.stop():
                contr.start()
            else:
                contr.step()
                contr.strats[contr.cur].step()
            time.sleep(1./env.clockPace)
    else:
        if env.isRunning:
            time.sleep(1./env.clockPace)
            updateContr(env, contr)

#############################################################

def main():
#Q1.1
    o1=Obstacle(10,20,10,30)
    o2=Obstacle()
    o3=Obstacle()
    o4=Obstacle()
    o5=Obstacle()


    robot = Robot(30,40,taille[0]*0.5,taille[1]*0.5)

    taille = (1024, 720)
    environnement = env(taille[0], taille[1], robot)

    environnement.addObstacle(o1)
    environnement.addObstacle(o2)
    environnement.addObstacle(o3)
    environnement.addObstacle(o4)
    environnement.addObstacle(o5)

#Q1.2

#Q1.3 ..
    
#Q1.4

from Agent.robot import Robot as rob
from Env.environnement import Environnement as env
from Controleur.avancerSansCollision import AvancerSansCollision as asc
########
from Controleur.tournerDirecte import TournerDirecte
#######
class ControleurCollision90():
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
        #Q1.4
            TournerDirecte(90, self.robot)
            return
        if self.cur<0 or self.strats[self.cur].stop():
            self.robot.setVitesseRoue(self.speed,self.speed)
            self.cur+=1
    
    def stop(self):
        """
            Condition d'arrêt de step
        """
        return self.cur == len(self.strats)-1 and self.strats[self.cur].stop()
#Q1.5
    #.....

#Q2.1
    class ballon:
        def __init__(self,width:int, length:int,vecteurDirecteur = Vecteur(0,-1), x:float=0, y:float=0) -> None:
            self.width=width
            self.length=length
            self.vd=vecteurDirecteur
            self.vitesseb=0
            self.position=(x,y)


        def vitesse(self,robot:rob):
            if (self.vitesseb!=rob.calcVitesseMoyenne):
                self.vitesseb=2*rob.calcVitesseMoyenne
            else:
                self.vitesseb=2*rob.calcVitesseMoyenne+self.vitesse
#Q2.2
        def touche(self,robot:rob,envir:env):

            if(self.position==robot.posCenter):

                self.vitesseb=0

    pass