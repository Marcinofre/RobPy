# -IMPORT ZONE---------------------------------------------------------------------------
from src.model.robot import Robot
import math
import logging
# ---------------------------------------------------------------------------------------

# -Logging setup-------------------------------------------------------------------------

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

# Niveau de logging
logger.setLevel(logging.INFO)

# Enregistrement dans un fichier
file_handler = logging.FileHandler("log/unitstrats.log")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# Flux destiné au terminal
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
# ---------------------------------------------------------------------------------------



# ----------------------------------------------------------------------------
class UnitStrat:
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
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
class MoveForward(UnitStrat):
	"""Stratégie unitaire qui fait avancer

		Stratégie permettant de faire avancer le robot sur une distance donnée en parametre

		Attributes:
			_robot (Robot): Robot qui est sujet à la stratégie
			_distance (int): Distance à parcourir
			_speed (float): Vitesse du robot
			stop_strat (bool): Condition d'arret a destination du lanceur de stratégie
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
		self._start = False
		self.stop_strat = False

	def start(self):
		"""Initialisation de la stratégie
		"""
		# On arrête le robot avant de commancer la stratégie
		self._robot.set_speed()
		self._robot.reset()

		
	def step(self):
		"""Exécution de la stratégie
		"""
		if not self._start :
			self._start = True
			self.start()
		# Observe si la distance à parcourir a été atteinte
		if self.stop():
			
			value = self._distance - self._robot._distance_traveled
			
			# Verification si le robot à trop avancer
			if abs(value) <= 0.01:							# ---> Pour le robot irl : 1, le simulé : 0.01
				# On éteint les moteurs
				self._robot.set_speed()
				self._robot.reset()

				self.stop_strat = True
				print("FIN")
				return
			else:
				speed = self._speed/2
				self._robot.set_speed(-speed, -speed)

				#Decommenter pour le robot irl
				#time.sleep(0.5)
				self._speed /= 2

		else:
			self._robot.set_speed(self._speed, self._speed)

		self._robot.get_distance_traveled()


			

	def stop(self):
		"""Condition d'arrêt de la stratégie en cours
		"""
		return (self._distance - self._robot._distance_traveled) <= 0


# ----------------------------------------------------------------------------
class RotateInPlace(UnitStrat):
	"""Pivote sur place le robot à gauche ou à droite

		Attributes:
			_robot (Robot): Robot sujet à la stratégie
			_speed (int): Vitesse du robot lors de la stratégie
			_theta_final (float): L'angle de rotation final que doit avoir robot à la fin de la simulation 
			angle (int): Angle de rotation à effectuer
			stop_strat (bool): Condition d'arret a destination du lanceur de stratégie

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
		self._start = False
		self.stop_strat = False
		self.left_right = (0,0)

	def start(self):
		"""Initialisation de la stratégie
		"""
		# On arrête le robot avant de commencer la stratégie et on initialise le theta_final à 0
		self._robot.set_speed()
		self._robot.reset()
		self._theta_final = 0

		
	def step(self):
		"""Exécution de la stratégie
		"""

		if not self._start :
			self._start = True
			self.start()
		# Si le theta n'est pas initialisé
		if self._theta_final == 0:
			
			# On calcule l'angle final au départ de la stratégie
			self._theta_final = self._robot._total_theta + math.radians(self.angle)
			logger.info(f"Degree à atteindre :  {math.degrees(self._theta_final)}")
			logger.info(f"Valeur de l'angle actuelle du robot  :  {math.degrees(self._robot._total_theta)}")


		
		
		# Observe si l'angle à parcourir a été atteint
		if self.stop():
			value = math.degrees(self._theta_final - self._robot._total_theta)
			if abs(value) <= 0.01:
				self._theta_final = 0
				# On éteint les moteurs
				self._robot.set_speed(0,0)
				self._robot.reset()
				self.stop_strat = True
				return 
			else:
				left, right = self.left_right
				self._robot.set_speed(self._speed * right, self._speed * left)
				# A décommenter pour le robot IRL
				#time.sleep(0.25)
				self._speed /= 2
		else:
			# Puis on active les moteurs selon l'angle final
			if self._theta_final > self._robot._total_theta:
				
				# On allume les moteur pour tourner a gauche
				self._robot.set_speed(-self._speed, self._speed)
				self.left_right = (-1,1)
			else:

				# On allume les moteur pour tourner a droite
				self._robot.set_speed(self._speed, -self._speed)
				self.left_right = (1,-1)
				

		self._robot.get_angle()

	
	def stop(self) -> bool:
		"""Condition d'arrêt de la stratégie en cours
		"""
		return math.degrees(self._theta_final - self._robot._total_theta) <= 0



# ----------------------------------------------------------------------------
class MoveForwardWithSensor(UnitStrat):
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
		self._start = False
		self.stop_strat = False

	def start(self):
		"""Initialisation de la stratégie
		"""
		# On arrête le robot avant de commancer la stratégie
		self._robot.set_speed()

		
	def step(self):
		"""Exécution de la stratégie
		"""
		if not self._start :
			self._start = True
			self.start()

		# Observe si la distance à parcourir a été atteinte
		if self.stop():
			# On éteint les moteurs
			self._robot.set_speed()
			self.stop_strat = True
			return
		else:
			self._robot.set_speed(self._speed, self._speed)
			

	def stop(self):
		"""Condition d'arrêt de la stratégie en cours
		"""
		return self._robot.get_distance() <= self._distance_stop