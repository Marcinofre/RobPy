from Env.environnement import Environnement as env
from Env.environnement import Obstacle
from Agent.robot import Robot
from utils.interface import Interface
from Controleur.controleurCarre import ControleurCarre
from Controleur.controleurCollision import ControleurCollision
from Agent.robotAdapteur import robotAdapteur
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

######################################################################################################################################
        
def main():
    ##Script de lancement de la simulation

    interfaceOn = introductionSimulation()

    print("Initialization in progress")


    #Définition de la taille de l'environnment
    taille = (1024, 720)

    #Définition du vecteur directeur initial du robot, puis du robot
    robot = Robot(30,40,taille[0]*0.5,taille[1]*0.5)
    robotA = robotAdapteur(30,40,taille[0]*0.5,taille[1]*0.5)

    #Initialisation de l'environnment
    environnement = env(taille[0], taille[1], robotA)

    #Initialisation du controleur du robot
    controleurCollision = ControleurCollision(robotA,environnement)
    controleurCarre = ControleurCarre(robotA)

    #Initialisation de l'interface graphique et lancement
    if interfaceOn :
        sim = Interface(environnement,controleurCarre)
        #sim = Interface(environnement,controleurCollision)
        #sim.add_obstacle(Obstacle(400,200,600,180))

    #environnement.addObstacle(Obstacle(400,200,600,200))
    updateE = threading.Thread(target=updateEnv, args=(environnement,))
    updateC = threading.Thread(target=updateContr, args=(environnement, controleurCarre))
    #updateC = threading.Thread(target=updateContr, args=(environnement, controleurCollision))


    #Lancemement de la simulation SANS interface
    if not interfaceOn:
        #Lancement des threads
        updateE.start()
        updateC.start()
        robotA.isControlled = True
        
        while True:
            input('--->>>>Press any key to stop<<<<---\n\n\n')
            environnement.isRunning = False
            robotA.isControlled = False
            break

    #Lancement de la simulation AVEC interface
    if interfaceOn:
        
        #Lancement des threads
        updateE.start()
        updateC.start()

        #Affichage de la fenetre
        sim.display_interface()


if __name__ == "__main__":
	main()
