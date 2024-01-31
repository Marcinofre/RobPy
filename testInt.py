from Environnement import Environnement as env
from Robot import Robot as rob
from Vecteur import Vecteur as vect
from Obstacle import Obstacle
from Interface import Interface

r = rob(75,125)

int = Interface(750, 1250, r)
obs = Obstacle(241,134,201,-100)
int.ajoutObstacle(obs)
int.affiche()