# -IMPORT ZONE---------------------------------------------------------------------------
import math
import threading
import time
from .model.robot import Robot, RobotAdapter, RobotFake
from .environment.environment import Environment, Obstacle, Interface
from .controller.controller import SequentialController
from .controller.strategies.unitstrats import unitStrat
from .controller.strategies.metastrats import StratSquare, StratDontTouchTheWall

# -CONSTANCE ZONE---------------------------------------------------------------------------

STRATS_VIRTUAL_ROBOT = [StratSquare,StratDontTouchTheWall]
STRATS_REAL_ROBOT = [StratSquare]

# -FUNCTION ZONE---------------------------------------------------------------------------
def update(fps: int , env: Environment, controller: SequentialController) -> None:
	"""Boucle d'update qui engage les mise jour de l'environnement et de ses composants

		On initialise le controleur (afin qu'il initilise les tratégies)
		L'update se déroule comme suit:
			- Update de l'environnement
			- Update du controleur
			-> Si l'ensemble des stratégies à été réalisé alors, on arrête la simulation

		Args:
			fps (int): Taux de rafraichissement de l'update de l'environnement/simulation
			env (Environnement): Environnement de la simulation
			controller (SequentialController): Controleur séquenciel (lanceur de stratégie)
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