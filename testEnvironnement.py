import unittest
from Robot import Robot as rob
from Environnement import Environnement as env


class Environnement(unittest.TestCase):
	def test_runAgent(self):
		r = rob(0,0,0,0)
		e = env(100,100, r)
		
		
		
		with self.assertRaises(Exception):
			r.isActivate = False
			e.runAgent(r,"scriptRobot.txt")
		
		r.isActivate = True
		
			
			

if __name__ == "__main__":
	unittest.main()