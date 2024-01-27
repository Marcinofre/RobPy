from Robot import Robot as r
from Vecteur import Vecteur as vec
import unittest

class Robot(unittest.TestCase) :
	
	def test_avancerRobot(self):
		robot = r(0,0,0,0)
		robot.vectD = vec(0.1, 0)
		robot.vectV = vec(1,2)
		
		print(robot.vectV.calcNorm())
		robot.avancerRobot()
		print(robot.posCenter)
		


if __name__ == "__main__":
	unittest.main() 