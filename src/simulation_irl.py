# -IMPORT ZONE---------------------------------------------------------------------------
import math
import threading
import time
import logging

try:
	from robot2IN013 import Robot2IN013
except Exception as e:
    print("IMPORTION FAILED")
    print(e)
    exit()
	
from .model.robot import Robot, RobotAdapter
from .environment.environment import Environment
from .controller.seqstrat import SequentialStrategy
from .controller.strategies.unitstrats import UnitStrat
from .controller.strategies.metastrats import StratSquare, StratDontTouchTheWall, MoveForwardOnly, RotateOnly

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
STRATS_REAL_ROBOT = [StratSquare, MoveForwardOnly, RotateOnly, StratDontTouchTheWall]

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
		print(f"value theta = {math.degrees(env._robot._total_theta)}")
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

	# On observe si le robot est un robot simulé ou un robot enrober par un adaptateur
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
			logger.error("Error : Wrong Number Index")
			continue
		except ValueError :
			logger.error("Error : Not a Number")
			continue
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
		

	robotReal = Robot2IN013()
	robot = RobotAdapter(robotReal, 0)

	# Intialisation de l'environnement de simulation
	environment = Environment(robot, size)

	choosen_strats = user_strat_choice(robot)

	# On initialise le controleur avec une stratégie ou liste de stratégie définit au niveau de metastrats.py ou unitstrats.py
	controller = SequentialStrategy(strats=choosen_strats)

	# On lance le thread relatif aux updates en indiquant le taux de rafraichissement de l'environnment
	update_t = threading.Thread(target=update, args=(fps, environment, controller))
	update_t.start()

