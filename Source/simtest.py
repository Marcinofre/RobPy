from Module.Env.Environnement import Environnement as env
from Module.Agent.Robot import Robot as rob
from Module.Vecteur import Vecteur as vect

r = rob(0,0,0,0)
e = env(100,100, r)
r.vectD = vect(1,1)

#Activation de l'agent
e.runEnv()
e.activateAgent(r)
e.runAgent(r,"scriptCarre.txt")


