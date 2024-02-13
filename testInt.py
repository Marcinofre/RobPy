from Module.Env.Environnement import Environnement as env
from Module.Vecteur import Vecteur as vect
from Module.Agent.Robot import Robot
from Module.Interface import Interface
from Module.Env.Environnement import Environnement as env
from Module.Contr.ControleurCarré import ControleurCarré as contrcar
import time

#Initialisation interface, Robot et Environnment
r = Robot(30,40,180,180)
r.vectD = vect(0,-15)
e = env(1024, 720, r)
c = contrcar(e)
sim = Interface(e,c)
sim.affiche()

