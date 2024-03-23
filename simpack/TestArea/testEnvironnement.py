import unittest
from simpack.Agent.robot import Robot as rob
from simpack.Env.environnement import Environnement as env
from simpack.utils.vecteur import Vecteur as vec
from simpack.Env.environnement import Obstacle as obs


class Environnement(unittest.TestCase):
	
	def test_ajoutObstacle(self):
		r = rob(0,0,0,0)
		e = env(100,100, r)
		o = obs(2, 2, 5, 5)
		
		e.addObstacle(o)
		self.assertTrue(o in e.setObstacle)

	def test_doesCollide(self) :
		r = rob(0,0,0,0)
		e = env(100,100, r)
		o = obs(2, -1, 1, 1)
		e.addObstacle(o)
		
		r.vectD.x = 2
		r.vectD.y = 0
		self.assertTrue(e.doesCollidebis())


			
			

if __name__ == "__main__":
	unittest.main()