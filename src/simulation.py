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
