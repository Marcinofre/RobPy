from Module.Env.Environnement import Environnement as env
from Module.Vecteur import Vecteur as vect
from Module.Agent.Robot import Robot
from Module.Interface import Interface
from Module.Env.Environnement import Environnement as env
#from Module.Contr.ControleurCarre import ControleurCarre
from Module.Contr.AvancerSansCollision import AvancerSansCollision
from Module.Env.Obstacle import Obstacle

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

    if response in ["yes", "y"]:
        return True
    else:
        return False

def updateEnv(env):
    """
        Update l'ensemble des classe de la simulation
    """
    env.initSimulation()
    while env.isRunning :
        env.update()			        #---> Update l'environnement
        time.sleep(1./env.clockPace)	#---> frame par sec 

def updateContr(env, contr):
    if contr.isActive:
        while env.isRunning and contr.isActive:
            if contr.stop():
                contr.start()
                updateContr(env, contr) 
            else:
                contr.step()
                contr.strats[contr.cur].step()
            time.sleep(1./env.clockPace)
    else:
        if env.isRunning:
            time.sleep(1./env.clockPace)
            updateContr(env, contr)

######################################################################################################################################
        

##Script de lancement de la simulation

interfaceOn = introductionSimulation()

print("Initialization in progress")


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
if interfaceOn :
    sim = Interface(environnement,controleurRobot)
    sim.ajoutObstacle(Obstacle(400,200,600,180))

environnement.addObstacle(Obstacle(400,200,600,200))
updateE = threading.Thread(target=updateEnv, args=(environnement,))
updateC = threading.Thread(target=updateContr, args=(environnement, controleurRobot))


#Lancemement de la simulation SANS interface
if not interfaceOn:
    
    #Lancement des threads
    updateE.start()
    updateC.start()
    
    while True:
        input('--->>>>Press any key to stop<<<<---\n\n\n')
        environnement.isRunning = False
        break

#Lancement de la simulation AVEC interface
if interfaceOn:
    
    #Lancement des threads
    updateE.start()
    updateC.start()

    #Affichage de la fenetre
    sim.affiche()


 
