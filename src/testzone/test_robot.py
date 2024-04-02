import math
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
from src.model.robot import Robot

class TestRobot(unittest.TestCase):
	def setUp(self):
		self.robot = Robot(x=0, y=0, theta=0)
	
	def test_update_position(self):
		# Initialisation des valeurs de test
		self.robot.get_time_passed = MagicMock(return_value=0.1)
		self.robot.get_speed = MagicMock(return_value=10)
		self.robot.get_angular_speed = MagicMock(return_value=math.pi / 4)

		# Appel de la fonction à tester
		self.robot.update_position()

		# Vérification des résultats attendus
		expected_x = 10 * math.cos(0) * 0.1
		expected_y = -10 * math.sin(0) * 0.1
		expected_theta = math.pi / 4 * 0.1
		self.assertAlmostEqual(self.robot._position_x, expected_x, delta=0.001)
		self.assertAlmostEqual(self.robot._position_y, expected_y, delta=0.001)
		self.assertAlmostEqual(self.robot._total_theta, expected_theta)


	@patch('time.time')
	def test_get_time_passed_first_call(self, mock_time):
		mock_time.return_value = 0
		dtime = self.robot.get_time_passed()
		self.assertEqual(dtime, 0)

	@patch('time.time')
	def test_get_time_passed_second_call(self, mock_time):
		# Initialisation avec le premier appel (modification de la var _last_update)
		mock_time.return_value = 10
		dtime = self.robot.get_time_passed() 
		
		# Vérification que le deuxième appel nous donne bien le temps entre le premier et second appel
		mock_time.return_value = 20
		dtime = self.robot.get_time_passed()  
		
		self.assertEqual(dtime, 10)

	def test_get_vector_dir(self):
		# Initialisation des valeurs de test
		self.robot._total_theta = math.pi / 4  # Angle de rotation du robot

		# Appel de la fonction à tester
		vector_dir = self.robot.get_vector_dir()

		# Vérification des résultats attendus
		expected_x = 20 * math.cos(-math.pi / 4)
		expected_y = 20 * math.sin(-math.pi / 4)
		self.assertAlmostEqual(vector_dir[0], expected_x, delta=0.001)
		self.assertAlmostEqual(vector_dir[1], expected_y, delta=0.001)

	def test_get_vector_captor(self):
		# Initialisation des valeurs de test
		self.robot._total_theta = math.pi / 4  # Angle de rotation du robot
		self.robot._captor_theta = math.radians(90)  # Angle de rotation du capteur
	   
		# Appel de la fonction à tester
		vector_captor = self.robot.get_vector_captor()

		# Vérification des résultats attendus
		expected_x = 1 * math.cos(-(math.pi / 4) + math.radians(90) - math.radians(90))
		expected_y = 1 * math.sin(-(math.pi / 4) + math.radians(90) - math.radians(90))
		self.assertAlmostEqual(vector_captor[0], expected_x, delta=0.001)
		self.assertAlmostEqual(vector_captor[1], expected_y, delta=0.001)

	def test_get_angular_speed(self):
		# Initialisation des valeurs de test
		self.robot._motorspeed_right = 10  # Vitesse du moteur droit
		self.robot._motorspeed_left = 5  # Vitesse du moteur gauche
		self.robot._WHEELBASE = 20  # Base de roue

		# Appel de la fonction à tester
		angular_speed = self.robot.get_angular_speed()

		# Calcul de la vitesse angulaire attendue
		expected_angular_speed = (10 - 5) / 20

		# Vérification des résultats attendus
		self.assertAlmostEqual(angular_speed, expected_angular_speed, delta=0.001)

	def test_get_distance_traveled(self):
		# Initialisation des valeurs de test
		self.robot._trail_position = [(0, 0), (3, 4), (6, 8)]  # Positions du robot

		# Appel de la fonction à tester
		distance = self.robot.get_distance_traveled()

		# Calcul de la distance parcourue attendue
		expected_distance = math.sqrt((6 - 3)**2 + (8 - 4)**2)

		# Vérification des résultats attendus
		self.assertAlmostEqual(distance, expected_distance, delta=0.001)

	def test_get_corners(self):
		# Initialisation des valeurs de test
		self.robot.get_position = MagicMock(return_value = (0, 0))  # Position du robot
		self.robot._total_theta = 0  # Angle de rotation du robot
		self.robot._dim = (40, 30)  # Dimensions du robot

		# Appel de la fonction à tester
		corners = self.robot.get_corners()

		# Vérification des résultats attendus
		expected_corners = [(20, 15), (20, -15), (-20, -15), (-20, 15)]
		self.assertListEqual(corners, expected_corners)

if __name__ == '__main__':
	unittest.main()