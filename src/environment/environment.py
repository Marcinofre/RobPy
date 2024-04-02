#----Import zone-----------------------------------
import math
import tkinter
import itertools
from src.model.robot import Robot
#--------------------------------------------------

class Obstacle:
	"""Class Obstacle qui représente un obstacle dans un environnement

		Attributes:
			origin (tuple[int, int]): Point d'origine de la diagonale de l'obstacle
			end (tuple[int, int]): Point de fin de la diagonale de l'obstacle

	"""

	def __init__(self, points: (list[tuple[int,int]])) -> None:
		"""Constructeur d'une instance Obstacle 
			
			Args:
				args (list[tuple[int,int]]): list de point contenant les deux point de la diagonale d'un rectangle
				
		"""
		self.origin = points[0]
		self.end = points[1]

	def make_rect_point(self) -> list[tuple[int,int]]:
		"""Retourne le rectangle formé par les deux point de la diagonale
		"""
		org_x, org_y = self.origin
		end_x, end_y = self.end
		points = [(x, y) for x in range(org_x, end_x + 1) for y in range(org_y, end_y + 1)]
		return points
	
	
	
	#def get_all_point(self) ->list[tuple[int,int]]:
	#	"""Rends l'ensemble des points qui constitue le périmètre de l'obstacle
	#	"""
	#
	#		# "Trie" la liste de points
	#	self.sort_points(self.list_of_points)
	#
	#		 


	#	pass

	#def sort_points(self) -> list[tuple[int,int]]:
		#"""Trie les points de tel sorte que s'il sont relier un à un, aucun croisement n'est possible

		#	Possible ressource/hint pour un algo de ce type :
		#		Probleme de l'enveloppe convexe ? https://fr.wikipedia.org/wiki/Calcul_de_l%27enveloppe_convexe
		#			-> Ne relie pas tout les points de la figure
		#		Trier par plus petit chemin ? 
		#			-> Ne fonctionne pas avec une forme en S croissante
		#		Trier par plus grand des deux plus petit chemin ? 
		#			-> Ne fonctionne pas pour un losange...
		#"""
		#pass


class Environment:
	"""Class Environment qui représente le lieu de la simulation dans lequel évolue un robot
	
		Attributes:
			_area_max (tuple[int,int]): Taille maximale de l'environnement
			_robot (Robot): Robot qui évolue dans l'environnement
			_obstacles (list[Obstacle]): Liste d'obstacle qui se peuple l'environnement
			_grid_obstacles (list[list[int]]): Matrice qui représente l'environnement et ses obstacles sous forme discrète
			stop (bool): Booleen qui permet d'arreter la simulation lorsque sa valeur True
	"""

	def __init__(self, robot: Robot, border_point: tuple[int,int] = (1280, 720)) -> None:
		"""Constructeur de l'environnement de la simulation

			Args:
				border_point (tuple[int,int]): Point maximale de l'environnement
				robot (Robot): Un robot
		"""

		# Dimension de l'Arene
		self._area_max = border_point

		# Ajout du robot passé en paramètre 
		self._robot = robot

		# Initialisation de la liste des obstacle de l'environnement (vide initialement) et de son positionnement dans la grille
		self._osbtacles = []
		self._grid_obstacles = [[0 for y in range(border_point[1])] for x in range(border_point[0])]
		
		# Condition d'arret de la simulation
		self.stop = False

	def add_obstacle(self, obs: Obstacle) -> None:
		"""Ajoute des obstacles à l'environnement

			Modifie la grille `_osbtacles` et `_grid_obstacle`

			Args: 
				obs (Obstacle): Un obstacle
		"""
		# On ajoute l'obstacle à la liste d'obstacle
		self._osbtacles.append(obs)

		# On récupère la liste de points innaccessible 
		obstacle_zone = obs.make_rect_point()
		
		# On map les obstacles sur la grille d'obstacle
		for x,y in obstacle_zone:
			self._grid_obstacles[x][y] = 1
	
	def get_obstacles(self) -> list[Obstacle]:
		"""Retourne la liste d'obstacle présent dans l'environnement
		"""
		return self._osbtacles

	def sensor_return(self) -> None:
		"""Simule le retour du capteur de distance
		"""

			# On récupère la position du robot et la direction du capteur
		pos_x, pos_y = self._robot.get_position()
		vect_sensor_x, vect_sensor_y = self._robot.get_vector_captor()

		# Pas du rayon
		step = 1
		
		# On boucle jusqu'à trouver un obstacle ou atteindre le maximum de step
		while step < 800 :
			try:
				if self._grid_obstacles[int(pos_x + vect_sensor_x*step)][int(pos_y + vect_sensor_y*step)]:
					#print(f"Obstacle rencontrer à {(int(pos_x + vect_sensor_x*step), int(pos_y + vect_sensor_y*step))}")
					#print(f"Distance de l'obstacle = {step}")
					self._robot._distance_obstacle = step
					return
			except IndexError:
				self._robot._distance_obstacle = -1
			step += 1
		self._robot._distance_obstacle = -1


	def is_out(self) -> bool:
		"""Détermine si le robot se trouve en dehors de la zone de la simulation

			Return:
				outside (bool): Bouléen qui exprime true s'il est en dehors ou false sinon 
		"""
		pos_x, pos_y = self._robot.get_position()
		arene_x,arene_y = self._area_max
		outside = (pos_x > arene_x) or (pos_y > arene_y) or (pos_x < 0) or (pos_y < 0)
		return outside
	
	def update_environment(self) -> None:
		"""Mets à jour l'ensemble de l'environnement
		"""
		
		if not self.stop:

		
			# Mise à jour du capteur de distance et la position du robot
			if isinstance(self._robot, Robot):
				self.sensor_return()
			self._robot.update_position()

			# Vérifie s'il touche un obstacle ou s'il est en dehors de la zone de simulation
			if self.is_out():

				# On remets le robot à sa place précédente (celle avant le 'choc')
				# On conserve la rotation cependant
				x,y = self._robot.get_last_position()
				self._robot.set_position(x, y)

