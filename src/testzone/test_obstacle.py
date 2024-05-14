import unittest
from model.environment import Obstacle

class TestObstacle(unittest.TestCase):
	def test_make_rect_point(self):
		# Initialisation des valeurs de test
		points = [(1, 1), (3, 3)]  # Points de la diagonale de l'obstacle
		obstacle = Obstacle(points)

		# Appel de la méthode à tester
		rect_points = obstacle.make_rect_point()

		# Vérification des résultats attendus
		expected_rect_points = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
		self.assertListEqual(rect_points, expected_rect_points)

if __name__ == '__main__':
	unittest.main()