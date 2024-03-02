from Module.Env.Environnement import Environnement as env
from Module.Vecteur import Vecteur as vect
from Module.Agent.Robot import Robot
from Module.Interface import Interface
from Module.Env.Environnement import Environnement as env
from Module.Contr.ControleurCarre import ControleurCarre
from Module.Contr.AvancerSansCollision import AvancerSansCollision
from Module.Env.Obstacle import Obstacle
import time
import threading

def updateEnv(env):
		"""
			Update l'ensemble des classe de la simulation
		"""
		env.initSimulation()
		while env.isRunning :
                        env.update()			#---> Update l'environnement
                        time.sleep(1./env.clockPace)	#---> frame par sec 

def updateContr(env, contr):
    while env.isRunning:
        if contr.stop():
            contr.start()
            updateContr(env, contr) 
        else:
            contr.step()
            contr.strats[contr.cur].step()
        time.sleep(1./env.clockPace)


##Script de lancement de la simulation

#Définition de la taille de l'environnment
taille = (1024, 720)
#Définition du vecteur directeur initial du robot, puis du robot
vecteurDirecteur = vect(0,-15)
robot = Robot(30,40,taille[0]*0.5,taille[1]*0.5,vecteurDirecteur)

#Initialisation de l'environnment
environnement = env(taille[0], taille[1], robot)

#Initialisation du controleur du robot
controleurRobot = AvancerSansCollision(robot,environnement)

#Initialisation de l'interface graphique et lancement
sim = Interface(environnement,controleurRobot)
sim.ajoutObstacle(Obstacle(400,200,600,180))
environnement.addObstacle(Obstacle(400,200,600,200))
updateE = threading.Thread(target=updateEnv, args=(environnement,))
updateC = threading.Thread(target=updateContr, args=(environnement, controleurRobot))
updateE.start()
updateC.start()
sim.affiche()