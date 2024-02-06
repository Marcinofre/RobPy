from Module.Env.Environnement import Environnement as env
from Module.Vecteur import Vecteur as vect
from Module.Agent.Robot import Robot
from Module.Interface import Interface
from Module.Env.Environnement import Environnement as env
import time
#Initialisation interface, Robot et Environnment
r = Robot(30,40,180,180)
r.vectD.x = 0
r.vectD.y = -15
e = env(1024, 720, r)
int = Interface(e.agent, e)


int.affiche()
r.vectD.x = 0
r.vectD.y = -10
