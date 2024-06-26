# -IMPORT ZONE---------------------------------------------------------------------------
import math
import threading
import time
import logging
from .model.robot import Robot, RobotAdapter, RobotFake
from .model.environment import Environment, Obstacle
from .view.interface2d import Interface
from .view.interface3d import Interface3D
from .controller.seqstrat import SequentialStrategy
from .controller.strategies.unitstrats import UnitStrat
from .controller.strategies.metastrats import StratSquare, StratDontTouchTheWall, MoveForwardOnly, RotateOnly, SearchOnly

# -Logging setup-------------------------------------------------------------------------

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

# Niveau de logging
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("log/simulation.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
# ---------------------------------------------------------------------------------------


# -CONSTANTE ZONE---------------------------------------------------------------------------
STRATS_VIRTUAL_ROBOT = [StratSquare,StratDontTouchTheWall, RotateOnly, SearchOnly]
STRATS_REAL_ROBOT = [StratSquare, MoveForwardOnly, RotateOnly, SearchOnly]

# -FUNCTION ZONE---------------------------------------------------------------------------
def update(fps: int , env: Environment, controller: SequentialStrategy) -> None:
	"""Boucle d'update qui engage les mise jour de l'environnement et de ses composants

		On initialise le controleur (afin qu'il initilise les tratégies)
		L'update se déroule comme suit:
			- Update de l'environnement
			- Update du controleur
			-> Si l'ensemble des stratégies à été réalisé alors, on arrête la simulation

		Args:
			fps (int): Taux de rafraichissement de l'update de l'environnement/simulation
			env (Environnement): Environnement de la simulation
			controller (SequentialStrategy): Controleur séquenciel (lanceur de stratégie)
	"""
	controller.start()
	while not env.stop:
		env.update_environment()
		controller.step()
		logger.info(env._robot.to_str())
		# Si le controller à terminer l'ensemble de ses stratégie alors on arrete la simulation 
		if controller.stop():
			env.stop = True
		time.sleep(1/fps)
		

def user_strat_choice(robot: Robot) -> list[UnitStrat]:
	"""Demande à l'utilisateur la métastratégie à appliquer

		Args:
			robot: Un robot pour savoir à quelle stratégie il a accès
	
		Return:
			strats_list (list[UnitStrat]): Une liste de stratégie unitStrat
	"""

	# Initialisation des variables
	meta_strat = None
	good_choice = False
	strats_list = []

	# On observe si le robot est un robot simulé ou un robot enrober par un adaptateur
	if isinstance(robot, Robot):
		possible_functions = STRATS_VIRTUAL_ROBOT
	else:
		possible_functions = STRATS_REAL_ROBOT


	# Demande à l'utilisateur le choix de la stratégie à appliquer
	print("Here the list of strat you can choose:")
	for strat in possible_functions:
		print(f"{strat.__name__} --> {possible_functions.index(strat)}")
	
	while (not good_choice):
		choice = input("Which strategy do you want to choose? (type the number) : ")
		try:
			meta_strat = possible_functions[int(choice)]
		except IndexError : 
			logger.error("Error : Wrong Number Index")
			continue
		except ValueError :
			logger.error("Error : Not a Number")
			continue
		else:
			good_choice = True

			# On récupère la liste issue de la métastratégie
			strats_list = meta_strat(robot)




	print(f"You choose {strats_list}")
	return strats_list


def simulation(size: tuple[int,int], fps: int) -> None:
	"""Simulation
		
		Args:
			size (tuple[int, int]): Taille de l'environnement (longueur, hauteur)
			fps (int): Taux de rafraichissement de l'environnement/simulation
	"""
	
	# Condition d'arrêt
	good_choice = False
	
	# Condition de l'interface
	interface = '0'
	interface2D = False
	interface3D = False

	while not good_choice:
		try:
			print("Robot mock/real --> 0 ")
			print("Robot simulé --> 1")

			robot_choice = input("Which robot do you want to use ?")
			
			if robot_choice not in ['0','1']:
				raise(IndexError)
			
			robot_choice = int(robot_choice)
		except IndexError :
			logger.error("Error : Wrong Number")
			continue
		except ValueError :
			logger.error("Error : Not a Number")
			continue

		good_choice = True


	if robot_choice:
		# Initialisation d'un robot 
		robot = Robot(size[0]*0.5,size[1]*0.5, math.radians(90))
		good_choice = False
		while not good_choice:
			try:
				print("None --> 0 ")
				print("2D --> 1")
				print("3D --> 2")

				interface = input("Which interface do you want to use ?")
				
				if interface not in ['0','1','2']:
					raise(IndexError)
			except IndexError :
				logger.error("Error : Wrong Number")
				continue
			except ValueError :
				logger.error("Error : Not a Number")
				continue
			good_choice = True
			
			if int(interface) == 1 :
				interface2D = True
			if int(interface) == 2:
				interface3D = True
	else:
		robotFake = RobotFake()
		robot = RobotAdapter(robotFake, math.radians(90))

	# Intialisation de l'environnement de simulation
	environment = Environment(robot, size)

	# ajoute un obstacle
	environment.add_obstacle(Obstacle([(0,0),(990,75)]))

	main_strat = user_strat_choice(robot)

	# On initialise le controleur avec une stratégie ou liste de stratégie définit au niveau de metastrats.py ou unitstrats.py
	controller = SequentialStrategy(strats=main_strat)

	# On lance le thread relatif aux updates en indiquant le taux de rafraichissement de l'environnment
	update_t = threading.Thread(target=update, args=(fps, environment, controller))
	update_t.start()
	
	if interface2D:
		# On initialise l'interface 
		gui = Interface(environment)
		gui.window.mainloop()
	if interface3D:
		app = Interface3D(environment)
		app.run()
