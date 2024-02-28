from Module.Env.Environnement import Environnement as env
from Module.Vecteur import Vecteur as vect
from Module.Chef import chef
from Module.Agent.Robot import Robot
from Module.Interface import Interface
from Module.Env.Environnement import Environnement as env
from Module.Contr.ControleurCarré import ControleurCarré 
from Module.Contr.ControleurCollision_bis import ControleurCollision



##Script de lancement de la simulation

#Définition de la taille de l'environnment
taille = (1024, 720)
#Définition du vecteur directeur initial du robot, puis du robot
vecteurDirecteur = vect(0,-15)
robot = Robot(30,40,taille[0]*0.5,taille[1]*0.5,vecteurDirecteur)

#Initialisation de l'environnment
environnement = env(taille[0], taille[1], robot)

#Initialisation du controleur du robot
controleurRobot = ControleurCollision(robot,environnement)

#Initialisation du controleur de la simulation (s'occupe de la mise a jour des composant de la simualtion)
controleurUpdate = chef(environnement,controleurRobot,10)

#Initialisation de l'interface graphique et lancement
sim = Interface(environnement,controleurRobot, controleurUpdate)
sim.affiche()
