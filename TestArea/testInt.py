from Module.Env.Environnement import Environnement as env
from Module.Vecteur import Vecteur as vect
from Module.Agent.Robot import Robot
from Module.Env.Obstacle import Obstacle
from Module.Interface import Interface
import time

r = Robot(75,125)

int = Interface(r)
obs = Obstacle(241,134,201,-100)

int.ajoutObstacle(obs)
r.posCenter = (150,150)
r.vectD.x = 0
r.vectD.y = -10
int.affiche()

