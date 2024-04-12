#----Import zone-----------------------------------
import math
import tkinter
import itertools
from src.model.robot import Robot
#--------------------------------------------------



#--CLASS Obstacle----------------------------------------
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
		#			-> Ne fonctionne pas pour un losange.
		#		Trier par plus grand des deux plus petit chemin ? 
		#			-> Ne fonctionne pas pour un losange...
		#"""
		#pass


#--ENVIRONMENT----------------------------------------
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
		self._obstacles = []
		self._grid_obstacles = [[0 for y in range(border_point[1])] for x in range(border_point[0])]
		
		# Condition d'arret de la simulation
		self.stop = False


	#-METHODE-------------------------------------------------------------------------------------------------
	def add_obstacle(self, obs: Obstacle) -> None:
		"""Ajoute des obstacles à l'environnement

			Modifie la grille `_obstacles` et `_grid_obstacle`

			Args: 
				obs (Obstacle): Un obstacle
		"""
		# On ajoute l'obstacle à la liste d'obstacle
		self._obstacles.append(obs)

		# On récupère la liste de points innaccessible 
		obstacle_zone = obs.make_rect_point()
		
		# On map les obstacles sur la grille d'obstacle
		for x,y in obstacle_zone:
			self._grid_obstacles[x][y] = 1
	
	def get_obstacles(self) -> list[Obstacle]:
		"""Retourne la liste d'obstacle présent dans l'environnement
		"""
		return self._obstacles

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




#--INTERFACE----------------------------------------
class Interface:
	"""Class Interface correspondant à la partie graphique de l'environnement (GUI)

		Attributes:
			Elements:
				env (Environment): Environnement de simulation à afficher
				robot (Robot): Robot qui se situe dans l'environnment

			Window:
				window (???): Fenetre Tkinter
				Composition:
					Drawing:
						frame_caneva (???): Frame Tkinter contenant le caneva
						caneva (???): Zone de dessin de la simulation
						display_robot (???): Polygone représentant le robot
						display_vect_line (???): Flèche représentant la direction du robot
					Text:
						frame_display (???): Zone d'affichage des informations relatif au robot qui évolue dans l'environnement
						info_display (???): ---
						info_label (???): Label des informations sur le robot (vitesse du moteur droit/gauche et son angle de rotation)

	"""


	#-CONSTRUCTEUR-------------------------------------------------------------------------------------------------
	def __init__(self, environment: Environment, dimension: tuple[int, int] = (1280, 720)) -> None:
		"""Constructeur d'une view pour afficher une simulation

			Args:
				environment (Environment): Environnement de la simulation
				dimension (tuple[int, int]): Taille de la fenetre 
		"""


		# Ajout de l'environment et du robot comme attribut
		self.env = environment
		self.robot = environment._robot
		
		# Creation de la fenetre principale
		self.window = tkinter.Tk(className="RobPy: The Simulation", )

		# On sépare la fenetre en deux zone 
		# Zone de simulation
		self.frame_caneva = tkinter.Frame(	self.window, 
											highlightbackground="black",
											highlightthickness=2)
		self.canvas = tkinter.Canvas(	self.frame_caneva, 
									 	height = self.env._area_max[1], 
									 	width = self.env._area_max[0], 
									 	bg = 'grey')
		
		self.frame_caneva.pack(side=tkinter.LEFT)
		self.canvas.pack()

		# Zone de texte
		self.frame_display = tkinter.Frame(	self.window, 
											height = dimension[1], 
											width = dimension[0]*0.2, 
											highlightbackground="black",
											highlightthickness=2)
		self.info_display = tkinter.Frame(self.frame_display)
		self.info_label = tkinter.Label(	self.info_display,
										 	text=f"Speed L : {self.robot._motorspeed_left}, Speed R : {self.robot._motorspeed_right}\nAngle {math.degrees(self.robot._total_theta)}° \nDistance Sensor {self.robot._distance_obstacle}")
		
		self.frame_display.pack(side=tkinter.RIGHT)
		self.info_display.pack()
		self.info_label.pack()

		# Dessin initiale sur le caneva
		robot_center = self.robot.get_position()
		vector = self.robot.get_vector_dir()
		vector_captor = self.robot.get_vector_captor()
		corners = self.robot.get_corners()
		obstacles = self.env.get_obstacles()
		
		self.display_robot = self.canvas.create_polygon(	
															*corners,
												  			fill="white",
															outline="black"
														)
		
		self.display_vect_line = self.canvas.create_line(	
															*robot_center,
												   			robot_center[0] + vector[0],
															robot_center[1] + vector[1],
															arrow=tkinter.LAST,
															width=5,
															fill='red'
														)
		
		self.display_vect_line2 = self.canvas.create_line(	
															*robot_center,
												   			robot_center[0] + vector_captor[0]*10,
															robot_center[1] + vector_captor[1]*10,
															arrow=tkinter.LAST,
															width=5,
															fill='blue'
														)
		
		# On ajoute les obstacles à la view
		for obs in obstacles:
			self.canvas.create_rectangle(
				obs.origin,
				obs.end,
				fill='black'
			)
		
		# Rappel de la fenetre
		self.window.after(50, self.update_tk)
	


	#-METHODE-------------------------------------------------------------------------------------------------
	def update_tk(self) -> None:
		"""Rafraichit l'affichage de la simulation
		"""
		# On récupère la position du robot, son vecteur et ses coins
		position = self.robot.get_position()
		vector = self.robot.get_vector_dir()
		vector_captor = self.robot.get_vector_captor()
		corners = self.robot.get_corners()
		
		# On redessine les éléments du robot avec leur nouvelles coordonnée
		self.canvas.coords(self.display_robot, 
						   *self.flatten(corners))
		
		self.canvas.coords(self.display_vect_line, 
						   *position,
						   position[0] + vector[0],
						   position[1] + vector[1])
		
		self.canvas.coords(self.display_vect_line2, 
						   *position,
						   position[0] + vector_captor[0]*10,
						   position[1] + vector_captor[1]*10)
		
		self.draw_path()
		self.update_label()
		self.window.after(50, self.update_tk)

	def update_label(self) -> None:
		"""Mise à jour des labels d'affichage
		"""
		self.info_label.config(text=f"Speed L : {self.robot._motorspeed_left}, Speed R : {self.robot._motorspeed_right} \nAngle {round(math.degrees(self.robot._total_theta), 5)}°\nDistance Sensor {self.robot._distance_obstacle}")

	#Voir source de cette fonction : https://stackoverflow.com/questions/32449670/tkinter-tclerror-bad-screen-distance-in-pythons-tkinter-when-trying-to-modi
	def flatten(self, list_of_lists):
		"""Flatten one level of nesting"""
		return itertools.chain.from_iterable(list_of_lists)

	def draw_path(self) -> None:
		"""Trace le passage du robot
		"""
		position = self.robot.get_position()
		self.canvas.create_oval(	
									position[0] - 2,
									position[1] - 2, 
									position[0] + 2, 
									position[1] + 2, 
									fill='blue' 
								)
