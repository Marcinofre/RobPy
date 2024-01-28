from Robot import Robot as r
from Vecteur import Vecteur as vec
import unittest

class Robot(unittest.TestCase) :
	
	def test_avancerRobot(self):
		robot = r(0,0,0,0)
		robot.vectD = vec(0.1, 0)
		
		
		robot.scalVitesse = 2.0
		for time in range(10):
			robot.avancerRobot()

		self.assertEqual(robot.posCenter, (round(2.0*0.1*10, 2), 0.0))
		
		robot.scalVitesse = 0
		robot.posCenter = (0.0,0.0)
		for time in range(10):
			robot.avancerRobot()
		self.assertEqual(robot.posCenter, (0.0, 0.0))

		robot.scalVitesse = 15
		robot.posCenter = (0.0,0.0)
		robot.vectD = vec(0.1, -4)
		for time in range(5):
			robot.avancerRobot()
		self.assertEqual(robot.posCenter, (7.5, -300.0))

		


if __name__ == "__main__":
	unittest.main() 