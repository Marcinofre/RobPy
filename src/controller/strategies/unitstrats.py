# -IMPORT ZONE---------------------------------------------------------------------------
from src.model.robot import Robot
import time
import cv2 as cv
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
	def __init__(self, distance: int, speed: float, robot: Robot, condition: bool = False):
		"""Constructeur de la stratégie moveForward

			Args:
				distance (int): Distance à parcourir
				speed (float): Vitesse du robot pendant la stratégie
				robot (Robot): Robot sur lequel s'applique la stratégie
		"""
		
		self._robot = robot
		self._speed = abs(speed)
		self._distance = abs(distance)
		self.condition = condition
		self._start = False
		self.stop_strat = False

	def start(self):
		"""Initialisation de la stratégie
		"""
		# On arrête le robot avant de commancer la stratégie
		self._robot.set_speed()
		self._robot.reset()
		logger.info("Initialisation de MoveForward") 

		
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
			if abs(value) <= 0.01 or self.condition:							# ---> Pour le robot irl : 1, le simulé : 0.01
				# On éteint les moteurs
				self._robot.set_speed()
				self._robot.reset()
				self.stop_strat = True
				
				logger.info("Fin de MoveForward") 
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
		return ((self._distance - self._robot._distance_traveled) <= 0) or self.condition

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
	def __init__(self, angle: int, speed: float, robot: Robot, condition: bool = False):
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
		self.condition = condition
		self._start = False
		self.stop_strat = False
		self.left_right = (0,0)


	def start(self):
		"""Initialisation de la stratégie
		"""
		# On arrête le robot avant de commencer la stratégie et on initialise le theta_final à 0
		self._robot.set_speed()
		self._robot.reset()
		self.condition = self._robot._beacon_in_sight
		self._theta_final = 0

		logger.info("Initialisation de RotateInPlace") 

		
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
			if (abs(value) <= 0.01) or self.condition:
				self._theta_final = 0
				# On éteint les moteurs
				self._robot.set_speed(0,0)
				self._robot.reset()
				self.stop_strat = True
				logger.info("Fin de RotateInPlace") 

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
		return (math.degrees(self._theta_final - self._robot._total_theta) <= 0) or self.condition

# ----------------------------------------------------------------------------
class MoveForwardWithSensor(UnitStrat):
	"""Avance le robot au plus près de l'obstacle
		
		Attributes:
			_robot (Robot): Robot qui est sujet à la stratégie
			_distance_stop (int): Distance d'arrêt au mur 
			_speed (float): Vitesse du robot
	"""

	def __init__(self, distance_stop: int, speed: float, robot: Robot, condition: bool = False):
		"""Constructeur de la stratégie moveForward

			Args:
				distance (int): Distance d'arrêt au mur
				speed (float): Vitesse du robot pendant la stratégie
				robot (Robot): Robot sur lequel s'applique la stratégie
		"""
		
		self._robot = robot
		self._distance_stop = distance_stop
		self._speed = abs(speed)
		self.condition = condition
		self._start = False
		self.stop_strat = False

	def start(self):
		"""Initialisation de la stratégie
		"""
		# On arrête le robot avant de commancer la stratégie
		self._robot.set_speed()
		logger.info("Initialisation de MoveForwardWithSensor") 


		
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
			logger.info("Initialisation de MoveForwardWithSensor") 

			return
		else:
			self._robot.set_speed(self._speed, self._speed)
			

	def stop(self):
		"""Condition d'arrêt de la stratégie en cours
		"""
		return (self._robot.get_distance() <= self._distance_stop) or self.condition
	
# ----------------------------------------------------------------------------
class SearchBalise(UnitStrat):
	"""Cherche une balise puis se dirige vers celle ci
	"""
	def __init__(self, robot):
		self._robot = robot
		self._servo_angle_start = 90
		self._start = False
		self.stop_strat = False
		self._balise = ["yellow", "green", "blue", "red", "white"]

	def start(self):
		"""Initialisation de la stratégie
		"""
		# On arrête le robot avant de commancer la stratégie
		self._robot.set_speed()
		self._robot.reset()
		self._robot.servo_rotate(self._servo_angle_start)
		self._robot.start_recording()
		logger.info("Initialisation de SearchBalise") 



	def step(self):
		
		# Cas initial
		if not self._start :
			self._start = True
			self.start()

		#Récupère l'image 
		chemin = self._robot.get_image()
		image = cv.imread(chemin)
		#Traitement de l'image : si pas de balise, tourne de 10 deg vers la gauche
		value = self._robot.search_balise_color(self._balise, image)
		print(f"Est-ce une balise ? {value} Bonne réponse ? -> {chemin}")
		if not self._robot.search_balise_color(self._balise, image):
			self._servo_angle_start -= 10
			print(f'rotation du servo : {self._servo_angle_start}')
			self._robot.servo_rotate(self._servo_angle_start)
		else:
			self._robot._beacon_in_sight = True

		# Cas d'arret
		if self.stop() :
			self._robot.stop_recording()
			self.stop_strat = True
			logger.info("Fin de SearchBalise")
			return

	def stop(self):
		return (self._servo_angle_start == -90) or self._robot._beacon_in_sight

class StratIf(UnitStrat):
	
	def __init__(self, robot: Robot, strat1: UnitStrat = None, strat2: UnitStrat = None, condition: bool = False):
		
		self.strat = Stop(robot)
		self._robot = robot 
		self._start = False
		self.stop_strat = False
		
		if not ((strat1 == None) and (strat2 == None)):
			if condition or self._robot._beacon_in_sight:
				self.strat = strat1
			else:
				self.strat = strat2
	
	def start(self):
		self.strat.start()
	
	def stop(self):
		self.strat.stop()

	def step(self):
		if not self._start:
			self.start()
		
		if self.strat.stop():
			self.stop_strat = True
			return
			
		self.strat.step()
		
class Stop(UnitStrat):
	"""Class abstraite
	"""
	def __init__(self, robot):
		self._robot = robot 
		self.stop_strat = False
	
	def start(self):
		pass

	def step(self):
		logger.info("STOP ROBOT")
		self._robot.set_speed()
		self.stop_strat = True
		return 

	def stop(self):
		stop_strat = True
		return True


	
