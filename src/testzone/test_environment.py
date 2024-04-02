import unittest
from src.model.robot import Robot
from src.environment.environment import Obstacle, Environment


class TestEnvironnement(unittest.TestCase):
	def setUp(self):
		self.robot = Robot(x=0, y=0, theta=0)  # Initialisation d'un robot
		self.env = Environment(robot=self.robot)  # Initialisation de l'environnement avec le robot

	def test_add_obstacle(self):
		# Ajout d'un obstacle à l'environnement
		obs = Obstacle([(1, 1), (3, 3)])
		self.env.add_obstacle(obs)

		# Vérification de l'ajout de l'obstacle
		obstacles = self.env.get_obstacles()
		self.assertEqual(len(obstacles), 1)
		self.assertIn(obs, obstacles)

	def test_sensor_return(self):
		# Simulation du retour du capteur de distance
		self.env.sensor_return()
		self.assertEqual(self.robot._distance_obstacle, -1)  # Ici, aucun obstacle n'est censé être détecté
		
		# Ajout d'un obstacle qui devrait être détecté
		obs = Obstacle([(5, 0), (5, 1)])  # Positionnant un obstacle à une distance de 5 de l'origine (0, 0)
		self.env.add_obstacle(obs)
		
		self.env.sensor_return()
		self.assertEqual(self.robot._distance_obstacle, 5)  # La distance de l'obstacle doit être de 5 unités

	def test_is_out(self):
		# Le robot est initialement à l'intérieur de la zone de simulation
		self.assertFalse(self.env.is_out())

		# Déplacement du robot en dehors de la zone de simulation
		self.robot._position_x = 1500
		self.robot._position_y = 1000

		# Vérification que le robot est maintenant en dehors de la zone de simulation
		self.assertTrue(self.env.is_out())

	def test_update_environment(self):

		# On fait un update
		self.env.update_environment()

		# Vérification de la mise à jour du capteur de distance et de la position du robot
		self.assertEqual(self.robot._distance_obstacle, -1)  # Le capteur de distance doit être mis à jour, mais aucun obstacle ne devrait être détecté dans cette configuration
		self.assertEqual(self.robot._position_x, 0)  # La position du robot ne devrait pas changer car il n'y a pas de collision ou de sortie de zone


if __name__ == '__main__':
	unittest.main()