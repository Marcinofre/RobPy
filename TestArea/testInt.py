from Module.Env.Environnement import Environnement as env
from Module.Vecteur import Vecteur as vect
from Module.Agent.Robot import Robot
from Module.Env.Obstacle import Obstacle
from Interface import Interface

r = Robot(75,125)

int = Interface(750, 1250, r)
obs = Obstacle(241,134,201,-100)
int.ajoutObstacle(obs)
int.affiche()