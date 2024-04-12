import math
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
from src.model.robot import RobotAdapter
from src.model.robot import RobotFake

class TestRobot(unittest.TestCase):
	def setUp(self):
		self.robot = RobotAdapter(RobotFake(),0)
	
	def test_get_angle(self):
		self.robot.set_speed(60,30)
		self.assertAlmostEqual(self.robot.get_angle(), 30)



if __name__ == '__main__':
	unittest.main()