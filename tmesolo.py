"""Lanceur de la simulation
"""
# -IMPORT ZONE--------------------------------------------------------------------------
from src.simulation import *

# -CONSTANTE---------------------------------------------------------------------------
SIZE_WORLD = (1024, 720)
FPS = 7000

# -APPLICATION PRINCIPALE--------------------------------------------------------------

def q1_1():
	# Ligne 261 dans environment.py
	simulation(SIZE_WORLD, FPS)

def q1_2():
	# Ligne 56,57 et 70 à 72 dans robot.py
 	simulation(SIZE_WORLD, FPS)

def q2_1():
	# Ligne 9 et 12 dans simulation.py
 	# Ligne 59 à 68 dans metastrats.py
	simulation(SIZE_WORLD, FPS)

def q2_2():
	# Ligne 9 et 12 dans simulation.py
 	# Ligne 71 à 82 dans metastrats.py
	simulation(SIZE_WORLD, FPS)

def q2_3():
	# Voir class MoveForwardWithSensor Ligne 151 dans unistrat.py puis décommenter le code rajouter
	# Dans metastrats.py
 	# Ligne 9 et 12 dans simulation.py
	simulation(SIZE_WORLD, FPS)

def q2_4():
	# Voir class MoveForwardWithSensor Ligne 151 dans unistrat.py puis décommenter le code rajouter
 	# Dans metastrats.py
	# Ligne 9 et 12 dans simulation.py
	simulation(SIZE_WORLD, FPS)

def q3_2():
	# Ligne 151 dans robot.py
 	simulation(SIZE_WORLD, FPS)
	 
def q3_1():
	# class gemme
	# 
 	simulation(SIZE_WORLD, FPS)

if __name__ == '__main__':
	main()