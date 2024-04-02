from src.model.robot import Robot
import math


class unitStrat:
	"""Class abstraite
	"""
	def __init__(self):
		pass
	
	def start(self):
		pass

	def step(self):
		pass

	def stop(self):
		pass
	pass

class MoveForward(unitStrat):
	"""Stratégie unitaire qui fait avancer

		Stratégie permettant de faire avancer le robot sur une distance donnée en parametre

		Attributes:
			_robot (Robot): Robot qui est sujet à la stratégie
			_distance (int): Distance à parcourir
			_speed (float): Vitesse du robot
	"""
	def __init__(self, distance: int, speed: float, robot: Robot):
		"""Constructeur de la stratégie moveForward

			Args:
				distance (int): Distance à parcourir
				speed (float): Vitesse du robot pendant la stratégie
				robot (Robot): Robot sur lequel s'applique la stratégie
		"""
		
		self._robot = robot
		self._speed = abs(speed)
		self._distance = abs(distance)
		self._distance_traveled = 0

	def start(self):
		"""Initialisation de la stratégie
		"""
		# On arrête le robot avant de commancer la stratégie
		self._robot.set_speed()

		
	def step(self):
		"""Exécution de la stratégie
		"""
		# Observe si la distance à parcourir a été atteinte
		if self.stop():
			# On éteint les moteurs
			self._robot.set_speed()
			return
		
		# Si le robot est à l'arrêt ou qu'il est a reculons, on le remets sur le droit chemin 
		if self._robot.get_speed() <= 0.0:
			
			self._robot.set_speed(self._speed, self._speed)


		#On ajoute la distance parcourue par la robot
		self._distance_traveled += self._robot.get_distance_traveled()
			

	def stop(self):
		"""Condition d'arrêt de la stratégie en cours
		"""
		return (self._distance - self._distance_traveled) <= 0.01
	
class RotateInPlace(unitStrat):
	"""Pivote sur place le robot à gauche ou à droite

		Attributes:
			_robot (Robot): Robot sujet à la stratégie
			_speed (int): Vitesse du robot lors de la stratégie
			_theta_final (float): L'angle de rotation final que doit avoir robot à la fin de la simulation 
			angle (int): Angle de rotation à effectuer

	"""
	def __init__(self, angle: int, speed: float, robot: Robot):
		"""Constructeur de la stratégie moveForward

			Args:
				angle (int): Angle de rotation à effectuer
				speed (float): Vitesse du robot pendant la stratégie
				robot (Robot): Robot sur lequel s'applique la stratégie
		"""
		
		self._robot = robot
		self._speed = speed
		self.angle =  angle
		self._theta_final = 0

	def start(self):
		"""Initialisation de la stratégie
		"""
		# On arrête le robot avant de commancer la stratégie et on initialise le theta_final à 0
		self._robot.set_speed()
		self._theta_final = 0 

		
	def step(self):
		"""Exécution de la stratégie
		"""
		
		# Observe si l'angle à parcourir a été atteint
		if self.stop():
			self._theta_final = 0
			# On éteint les moteurs
			self._robot.set_speed(0,0)
			return 
		
		# Si le theta n'est pas initialisé
		if self._theta_final == 0:
			
			# On calcule l'angle final au départ de la stratégie
			self._theta_final = self._robot._total_theta + math.radians(self.angle)

			# Puis on active les moteurs selon l'angle final
			if self._theta_final > self._robot._total_theta:
				
				#print("On allume les moteur pour tourner a gauche")
				self._robot.set_speed(-self._speed, self._speed)
			else:

				#print("On allume les moteur pour tourner a droite")
				self._robot.set_speed(self._speed, -self._speed)

	
	def stop(self) -> bool:
		"""Condition d'arrêt de la stratégie en cours
		"""
		return abs(self._theta_final - self._robot._total_theta) <= 0.001

class MoveForwardWithSensor(unitStrat):
	"""Avance le robot au plus près de l'obstacle
		
		Attributes:
			_robot (Robot): Robot qui est sujet à la stratégie
			_distance_stop (int): Distance d'arrêt au mur 
			_speed (float): Vitesse du robot
	"""

	def __init__(self, distance_stop: int, speed: float, robot: Robot):
		"""Constructeur de la stratégie moveForward

			Args:
				distance (int): Distance d'arrêt au mur
				speed (float): Vitesse du robot pendant la stratégie
				robot (Robot): Robot sur lequel s'applique la stratégie
		"""
		
		self._robot = robot
		self._distance_stop = distance_stop
		self._speed = abs(speed)

	def start(self):
		"""Initialisation de la stratégie
		"""
		# On arrête le robot avant de commancer la stratégie
		self._robot.set_speed()

		
	def step(self):
		"""Exécution de la stratégie
		"""
		# Observe si la distance à parcourir a été atteinte
		if self.stop():
			# On éteint les moteurs
			self._robot.set_speed()
			return
		
		# Si le robot est à l'arrêt ou qu'il est a reculons, on le remets sur le droit chemin 
		if self._robot.get_speed() <= 0.0:
			self._robot.set_speed(self._speed, self._speed)
			

	def stop(self):
		"""Condition d'arrêt de la stratégie en cours
		"""
		return self._robot.get_distance() <= self._distance_stop