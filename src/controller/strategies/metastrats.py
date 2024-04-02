from src.controller.strategies.unitstrats import *
from src.model.robot import Robot


def StratSquare(robot: Robot) -> list[unitStrat]:
	"""Stratégie pour faire parcourir au robot un carré de 50 par 50
	"""
	print("\n\n------INITIALISATION StratSquare------\n")
	good_choice = False
	while not good_choice:
		try:
			speed = int(input("Vitesse du robot : "))
		except ValueError:
			print("Error: Not a Number")
			pass

		try:
			distance = int(input("Distance de course par côté du robot : "))
		except ValueError:
			print("Error: Not a Number")
			pass
		good_choice = True

	return [MoveForward(distance, speed, robot),
			RotateInPlace(90, speed,robot),
			MoveForward(distance, speed, robot),
			RotateInPlace(90, speed,robot),
			MoveForward(distance, speed, robot),
			RotateInPlace(90, speed,robot),
			MoveForward(distance, speed, robot),
			RotateInPlace(90, speed,robot)]


def StratDontTouchTheWall(robot: Robot) -> list[unitStrat]:
	"""Stratégie pour aller vers un mur sans le toucher
	"""
	print("\n\n------INITIALISATION StratDontTouchTheWall------\n")
	good_choice = False
	while not good_choice:
		try:
			speed = int(input("Vitesse du robot : "))
		except ValueError:
			print("Error: Not a Number")
			pass

		try:
			distance_from_wall = int(input("Distance au mur : "))
		except ValueError:
			print("Error: Not a Number")
			pass
		good_choice = True

	return [MoveForwardWithSensor(distance_from_wall, speed, robot)]


def StratFollowTheLight(robot: Robot):
	pass