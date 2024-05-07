# -IMPORT ZONE---------------------------------------------------------------------------
import logging
from src.controller.strategies.unitstrats import MoveForward, MoveForwardWithSensor, RotateInPlace, UnitStrat
from src.model.robot import Robot
# ---------------------------------------------------------------------------------------


# -Logging setup-------------------------------------------------------------------------

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

# Niveau de logging
file_handler = logging.FileHandler("log/metastrat.log")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# ---------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------
def StratSquare(robot: Robot) -> list[UnitStrat]:
	"""Stratégie pour faire parcourir au robot un carré de 50 par 50
	"""
	print("\n\n------INITIALISATION StratSquare------\n")
	good_choice = False
	while not good_choice:
		try:
			speed = float(input("Vitesse du robot : "))
		except ValueError:
			logger.error("Error: Not a Number")
			continue
		
		try:
			distance = int(input("Distance de course par côté du robot : "))
		except ValueError:
			logger.error("Error: Not a Number")
			continue
		
		good_choice = True

	return [MoveForward(distance, speed, robot),
			RotateInPlace(90, speed,robot),
			MoveForward(distance, speed, robot),
			RotateInPlace(90, speed,robot),
			MoveForward(distance, speed, robot),
			RotateInPlace(90, speed,robot),
			MoveForward(distance, speed, robot),
			RotateInPlace(90, speed,robot)]

# ----------------------------------------------------------------------------
def StratDontTouchTheWall(robot: Robot) -> list[UnitStrat]:
	"""Stratégie pour aller vers un mur sans le toucher
	"""
	print("\n\n------INITIALISATION StratDontTouchTheWall------\n")
	good_choice = False
	while not good_choice:
		try:
			speed = int(input("Vitesse du robot : "))
		except ValueError:
			logger.error("Error: Not a Number")
			continue

		try:
			distance_from_wall = int(input("Distance au mur : "))
		except ValueError:
			logger.error("Error: Not a Number")
			continue
		good_choice = True

	return [MoveForwardWithSensor(distance_from_wall, speed, robot)]

# ----------------------------------------------------------------------------

def MoveForwardOnly(robot: Robot)-> list[UnitStrat]:
	"""Stratégie pour faire parcourir au robot un carré de 50 par 50
	"""
	print("\n\n------INITIALISATION MoveForwardOnly------\n")
	good_choice = False
	while not good_choice:
		try:
			speed = float(input("Vitesse du robot : "))
		except ValueError:
			logger.error("Error: Not a Number")
			continue
		
		try:
			distance = int(input("Distance de course: "))
		except ValueError:
			logger.error("Error: Not a Number")
			continue
		
		good_choice = True

	return [MoveForward(distance, speed, robot)]

def RotateOnly(robot: Robot)-> list[UnitStrat]:
	"""Stratégie pour faire un rotation de x degree
	"""
	print("\n\n------INITIALISATION RotateOnly------\n")
	good_choice = False
	while not good_choice:
		try:
			speed = float(input("Vitesse du robot : "))
		except ValueError:
			logger.error("Error: Not a Number")
			continue
		
		try:
			angle = int(input("Angle de rotation (deg): "))
		except ValueError:
			logger.error("Error: Not a Number")
			continue
		
		good_choice = True

	return [RotateInPlace(angle, speed, robot)]