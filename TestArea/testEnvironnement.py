import unittest
from Module.Agent.Robot import Robot as rob
from Module.Env.Environnement import Environnement as env
from Module.Vecteur import Vecteur as vec


class Environnement(unittest.TestCase):
	def test_runAgent(self):
		r = rob(0,0,0,0)
		e = env(100,100, r)
		
		
		
		with self.assertRaises(Exception):
			r.isActivate = False
			e.runAgent(r,"scriptRobot.txt")
		
		r.isActive = True
		e.runAgent(r, "fichierexistepasalorsrobotpasbouger")
		self.assertEqual(r.posCenter, (0,0))

		r.posCenter = (45,45)
		e.runAgent(r, "fichierexistepasalorsrobotpasbouger")
		self.assertEqual(r.posCenter, (45,45))

		r.posCenter = (0,0)
		r.vectD = vec(1,1)
		e.runEnv()
		e.runAgent(r, "AvancerToutDroit.txt")
		self.assertEqual(r.posCenter, (1,1))


			
			

if __name__ == "__main__":
	unittest.main()