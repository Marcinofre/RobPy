# -IMPORT ZONE---------------------------------------------------------------------------
import math
import threading
import time
from .model.robot import Robot, RobotAdapter, RobotFake
from .environment.environment import Environment, Obstacle, Interface
from .controller.controller import SequentialStrategy
from .controller.strategies.unitstrats import unitStrat
from .controller.strategies.metastrats import StratSquare, StratDontTouchTheWall, Strat_2_1, Strat_2_2, Strat_2_3, Strat_2_4

# -CONSTANTE ZONE---------------------------------------------------------------------------
STRATS_VIRTUAL_ROBOT = [StratSquare,StratDontTouchTheWall, Strat_2_1, Strat_2_2, Strat_2_3, Strat_2_4]
STRATS_REAL_ROBOT = [StratSquare]

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
		# Si le controller à terminer l'ensemble de ses stratégie alors on arrete la simulation 
		if controller.stop():
			env.stop = True
		time.sleep(1/fps)
		

def user_strat_choice(robot: Robot) -> list[unitStrat]:
	"""Demande à l'utilisateur la métastratégie à appliquer

		Args:
			robot: Un robot pour savoir à quelle stratégie il a accès
	
		Return:
			strats_list (list[unitStrat]): Une liste de stratégie unitStrat
	"""

	# Initialisation des variables
	meta_strat = None
	good_choice = False

	# On observe si le robot est un robot simulé ou un robot enrober par un adaptateur
	if isinstance(robot, Robot):
		possible_functions = STRATS_VIRTUAL_ROBOT
	else:
		possible_functions = STRATS_REAL_ROBOT


	# Demande à l'utilisateur le choix de la stratégie à appliquer
	print("Here the list of strat you can choose:")
	for strat in possible_functions:
		print(f"{strat.__name__} --> {possible_functions.index(strat)}")
	
	while not good_choice :
		choice = input("Which strategy do you want to choose? (type the number) : ")
		try:
			meta_strat = possible_functions[int(choice)]
		except IndexError : 
			print("Error : Wrong Number Index")
			pass
		except ValueError :
			print("Error : Not a Number")
			pass
		else:
			good_choice = True
	
	# On récupère la liste issue de la métastratégie
	strats_list = meta_strat(robot)

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
	interface = False

	while not good_choice:
		try:
			print("Robot mock/real --> 0 ")
			print("Robot simulé --> 1")

			robot_choice = input("Which robot do you want to use ?")
			
			if robot_choice not in ['0','1']:
				raise(IndexError)
			
			robot_choice = int(robot_choice)
		except IndexError :
			print("Error : Wrong Number")
			pass
		except ValueError :
			print("Error : Not a Number")
			pass

		good_choice = True


	if robot_choice:
		# Initialisation d'un robot 
		robot = Robot(size[0]*0.5,size[1]*0.5, math.radians(90))
		interface = True
	else:
		robotFake = RobotFake()
		robot = RobotAdapter(robotFake, math.radians(90))

	# Intialisation de l'environnement de simulation
	environment = Environment(robot, size)

	# AJOUTER ICI UNE FONCTION QUI AJOUTE UN NOMBRE D'OBSTACLES DISPOSER ALÉATOIREMENT SUR LE CANEVA
	environment.add_obstacle(Obstacle([(0,0),(990,75)]))
	
	choosen_strats = user_strat_choice(robot)

	# On initialise le controleur avec une stratégie ou liste de stratégie définit au niveau de metastrats.py ou unitstrats.py
	controller = SequentialStrategy(strats=choosen_strats)

	# On lance le thread relatif aux updates en indiquant le taux de rafraichissement de l'environnment
	update_t = threading.Thread(target=update, args=(fps, environment, controller))
	update_t.start()
	
	if interface:
		# On initialise l'interface 
		gui = Interface(environment)
		gui.window.mainloop()
