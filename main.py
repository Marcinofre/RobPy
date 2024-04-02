from simpack.Env.environnement import Environnement as env
from simpack.Env.environnement import Obstacle
from simpack.Agent.robot import Robot
from simpack.utils.interface import Interface
from simpack.Controleur.controleurCarre import ControleurCarre
from simpack.Controleur.controleurCollision import ControleurCollision
from simpack.Agent.robotAdapteur import robotAdapteur
from simpack.Agent.robotAdapteur import robotFake
import time


def introductionSimulation():
    """
        Affiche une introduction et retourne un bool selon si la simulation doit etre demarrer avec ou sans interface graphique depuis le terminal
    """
    print("The RobPy simulation is currently being initialized.")
    print("Please kindly follow the instructions that may follow")
    print("For each instruction, please write \"yes\" or (\"y\") or \"no\" (\"n\"). If another element is detected, it will be considered \"no\" as default")
    response = input("Do you want to start the simulation with the interface ?\n--->>>")

    return response in ["yes", "y"]

def runSimulation(interface, environnement, controleur):
    if not interface:
        environnement.initSimulation()
        while True:
            if not controleur.stop():
                environnement.update()
                controleur.step()
                controleur.strats[controleur.cur].step()
                time.sleep(1)
            elif controleur.stop():
                controleur.start()
    elif interface:
        interface.display_interface()

######################################################################################################################################
        
def main():
    ##Script de lancement de la simulation

    interfaceOn = introductionSimulation()

    print("Initialization in progress")

    #Définition de la taille de l'environnment
    taille = (1024, 720)

    #Définition du vecteur directeur initial du robot, puis du robot
    robot = Robot(30,40,taille[0]*0.5,taille[1]*0.5)
    robotA = robotAdapteur(robotFake())

    #Initialisation de l'environnment
    environnement = env(taille[0], taille[1], robotA)

    #Initialisation du controleur du robot
    controleurCollision = ControleurCollision(robotA,environnement)
    controleurCarre = ControleurCarre(robotA)


    #Lancemement de la simulation SANS interface
    if not interfaceOn:
        #Lancement des threads
        runSimulation(None, environnement, controleurCarre)

    #Lancement de la simulation AVEC interface
    if interfaceOn:
        if isinstance(environnement.agent, robotAdapteur):
            print("Erreur! On ne peut pas utiliser l'interface pour le robotAdapteur")
            print("Lancement de la simulation sans interface")
            time.sleep(1)
            runSimulation(None, environnement, controleurCarre)
        else :
            sim = Interface(environnement,controleurCarre)
            #sim = Interface(environnement,controleurCollision)
            #sim.add_obstacle(Obstacle(400,200,600,180))
            #environnement.addObstacle(Obstacle(400,200,600,200))
            runSimulation(sim, environnement, controleurCarre)


if __name__ == "__main__":
	main()


"""Lanceur de la simulation
"""
# -IMPORT ZONE--------------------------------------------------------------------------
from src.simulation import *

# -CONSTANTE---------------------------------------------------------------------------
SIZE_WORLD = (1024, 720)
FPS = 7000

# -APPLICATION PRINCIPALE--------------------------------------------------------------
def main():
	simulation(SIZE_WORLD, FPS)

if __name__ == '__main__':
	main()