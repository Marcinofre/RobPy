from src.Agent.robot import Robot
from src.Env.environnement import Environnement
from src.Env.environnement import Obstacle
from src.utils.interface import Interface 
from src.Controleur.controleurGenerique import ControleurGenerique
from src.Controleur.avancerDroit import AvancerDroit
import threading
import time

# Constante Définissant la taille de l'environnement dans un tuple avec sa longeur et sa hauteur 
TAILLE = (1024, 720)

#####################################################

# Permet les update de l'environnement et du controler

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
###########################################################
            

#Question 1.1 
def q1_1()-> None:
    """
        Réponse à la question 1.1
        Définition d'un environnement contenant 5 obstacles
    """

    # Robot factice

    robot_factice = Robot(25,25, TAILLE[0]*0.5, TAILLE[1]*0.5)

    # Création de l'environnement
    environment = Environnement(TAILLE[0], TAILLE[1], robot_factice)

    

    # Définition de 5 obstacles
    obst_1 = Obstacle(40,40,70,70)
    obst_2 = Obstacle(TAILLE[0]*0.75, TAILLE[1]*0.5-80,TAILLE[0]*0.5-70, TAILLE[1]*0.5-70)
    obst_3 = Obstacle(900,80,100,100)
    obst_4 = Obstacle(100,120,10,520)
    obst_5 = Obstacle(70,70,86,86)

    # Ajout des Obstacles
    environment.addObstacle(obst_1)
    environment.addObstacle(obst_2)
    environment.addObstacle(obst_3)
    environment.addObstacle(obst_4)
    environment.addObstacle(obst_5)

    # Initialisation de l'interface
    gui = Interface(environment, None, color_obstacle="orange")

    # Affichage de l'interface graphique
    gui.display_interface()

def q1_2() -> None:
    """
        La réponse de la question 1.2 est inclue dans le code 1.1.
    """
    # Exécute la commande 1.1
    q1_1()

def q1_3() -> None:
    """
        Les modifiacations on été apporté à interface qui désormais possède un bouton qui appelle la fonction dessine() qui mets a true ou false la variable self.draw. A false, il empeche le dessin d'etre update, à true il reprend les update de la trace normalement
    """

    # Robot factice
    robot_factice = Robot(25,25, TAILLE[0]*0.5, TAILLE[1]*0.5)

    # Création de l'environnement
    environment = Environnement(TAILLE[0], TAILLE[1], robot_factice)

    # Initialisation d'un controleur qui ne fait qu'avancer le robot sur une distance donné
    controler = ControleurGenerique([AvancerDroit(150, 5, robot_factice)])

    gui = Interface(environment, controler)

    # Initialisation des threads

    update_environment = threading.Thread(target=updateEnv, args=(environment,))
    update_controler = threading.Thread(target=updateContr, args=(environment, controler))


    # Activation des threads
    
    update_environment.start()
    update_controler.start()

    # Affichage de l'interface
    gui.display_interface()


def q1_4():
    """
        Configuration d'une stratégie comme décrit dans l'énoncé
    """

    # Robot factice
    robot_factice = Robot(25,25, TAILLE[0]*0.5, TAILLE[1]*0.5)

    # Création de l'environnement
    environment = Environnement(TAILLE[0], TAILLE[1], robot_factice)

    # Initialisation d'un controleur 
    controler = ControleurGenerique([AvancerDroit(5, 5, robot_factice), ])

    gui = Interface(environment, controler)

    # Initialisation des threads

    update_environment = threading.Thread(target=updateEnv, args=(environment,))
    update_controler = threading.Thread(target=updateContr, args=(environment, controler))


    # Activation des threads
    
    update_environment.start()
    update_controler.start()

    # Affichage de l'interface
    gui.display_interface()




    






if __name__ == "__main__":
    #q1_1()
    q1_3()

