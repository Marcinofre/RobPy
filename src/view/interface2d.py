from model.environment import Environment
import tkinter
import math
import itertools
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
