"""
	Class définissant le robot, le robotFake et son adaptateur qui sera utiliser dans l'environnement de simulation
"""

#- Import zone-----------------------------------
import math
import threading
import time
import numpy as np
import cv2 as cv
import os
import re
import random
import logging
#--------------------------------------------------

# -Logging setup-------------------------------------------------------------------------

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(asctime)s:%(name)s: %(message)s')

# Niveau de logging
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("log/robot.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)


logger.addHandler(file_handler)
logger.addHandler(stream_handler)
# ---------------------------------------------------------------------------------------


#- ROBOT------------------------------------------
class Robot:
	"""Class Robot qui définit un robot de licence d'Informatique de Sorbonne Université

		Attributes:
			_dim (tuple[int,int]): Dimension du robot longueur, largeur
			_wheelbase (int): Empatement entre les deux roues

			_position_x (float): Position courante du robot sur l'abcisse dans l'environnement virtuelle
			_position_y (float): Position courante du robot sur l'ordonnée dans l'environnement virtuelle
			_total_theta (float): Angle de rotation vis-à-vis du plan de l'environnement
			_current_theta (float): Angle courant (stratégie)
			_captor_theta (float): Angle de rotation du capteur vis-à-vis du plan du vecteur directeur


			_motorspeed_right (float): Vitesse du moteur droit
			_motorspeed_left (float): Vitesse du moteur gauche

			_trail_position (list[tuple[float, float]]): Tableau enregistrant toutes les positions du robot précédente
			_last_update (float): Temps de la dernière mise à jour effectué

	"""
	
	
	
	#- CONSTRUCTEUR-------------------------------------------------------------------------------------------------
	def __init__(self, x: float, y: float, theta: float) -> None:
		"""Constructeur de l'instance Robot
		
			Le constructeur se base sur les caractéristique réelles du robot attribué par l'université. Pour avoir de plus amples détails, merci de vous référer à sa fiche technique (voir lien: https://github.com/baskiotisn/2IN013robot2023/blob/main/docs/cours5.pdf)

			Args:
				x (float): Position initial en abscisse du robot
				y (float): Position initial en ordonnée du robot
				theta (float): Angle initial de rotation vis-à-vis du plan de l'environnement
		"""
		# Caractéristique constante du robot
		self._dim = (40,30)
		self._WHEELBASE = self._dim[1]

		# Position, angle et direction du robot dans l'environnement
		self._position_x = x
		self._position_y = y
		self._total_theta = theta
		self._captor_theta = math.radians(90)
		self._distance_obstacle = -1

		# Vitesse des moteurs initialisé à 0
		self._motorspeed_right = 0
		self._motorspeed_left = 0

		# Historique des positions du robot depuis le point de départ
		self._trail_position = [self.get_position()]

		# Temps de la dernière mise à jour, initialisé à 0 quand aucune mise à jour n'a été faite
		self._last_update = 0
		self._distance_traveled = 0

		# Balise dans le champs de vision false par défaut
		self._beacon_in_sight = False

	
	
	
	#- METHODE-------------------------------------------------------------------------------------------------
	def update_position(self) -> None:
		"""Mise à jour de la position du robot
		"""
		# Calcule du temps écoulé
		dtime = self.get_time_passed()

		# Calcule les nouvelles positions x et y, ainsi que l'angle de rotation selon la vitesse et le temps écoulé
		self._position_x += self.get_speed() * math.cos(self._total_theta) * dtime
		self._position_y -= self.get_speed() * math.sin(self._total_theta) * dtime
		self._total_theta += self.get_angular_speed() * dtime

		# Enregistrement de la nouvelle position
		self._trail_position.append(self.get_position())
		if len(self._trail_position) > 5:
			self._trail_position.pop(0)
			
	def get_angle(self):
		# On récupère la position des moteurs
		pass

	def get_time_passed(self) -> float:
		"""Calcule le temps passé entre le dernier appel et le temps courant

			Return:
				dtime (float): Correspond au temps écoulé depuis le dernier appel renseigné dans `self._last_update`
		"""
		# On initialise si c'est le premier appel
		if not self._last_update:
			self._last_update = time.time()
		
		# On calcule le temps écoulé depuis _last_update
		dtime = time.time() - self._last_update
		self._last_update = time.time()

		return dtime 
	
	def get_vector_dir(self) -> tuple[float, float]:
		"""Calcule le vecteur directeur pour apercevoir la direction du robot

			La taille du vecteur directeur ne correspond pas à sa vitesse, il n'est ici qu'a des fins de représentation. La taille est donc arbitraire et correspond ici à la longeur du robot

			Return:
				vector_dir (tuple[float, float]): Vecteur qui représente la direction que prend le robot
		"""
	
		# Calcule du vecteur direction
		vector_dir = (	self._dim[0]/2 * math.cos(-self._total_theta), 
						self._dim[0]/2 * math.sin(-self._total_theta))
		return vector_dir
	
	def get_vector_captor(self) -> tuple[float, float]:
		"""Calcule le vecteur directeur du capteur du robot

			La taille du vecteur directeur ne correspond pas à sa projection, il n'est ici qu'a des fins de représentation. La taille est donc arbitraire et correspond ici à une unité aribtraire

			Return:
				vector_captor (tuple[float, float]): Vecteur qui représente la direction vers laquel pointe le capteur
		"""
		# Permet d'obtenir un range de rotation entre -90 et 90 au lieu de 0 et 180
		rotation = self._captor_theta - math.radians(90)
	
		# Calcule du vecteur du capteur 
		vector_captor = (	1 * math.cos(-self._total_theta + rotation), 
							1 * math.sin(-self._total_theta + rotation))
		return vector_captor
	
	def get_distance(self) -> float:
		"""Renvoie la distance entre le robot et l'obstacle en face de lui

			Return:
				distance_obstacle (float): Distance entre l'obstacle et le robot. -1 si il ne rencontre aucun objet
		"""
		return self._distance_obstacle
	
	def set_speed(self, speed_left: float = 0, speed_right: float = 0) -> None:
		"""Modifie les vitesses des deux moteurs du robot
			
			Args:
				speed_left (float): Nouvelle vitesse du moteur gauche
				speed_right (float): Nouvelle vitesse du moteur droit
		"""
		self._motorspeed_left = speed_left
		self._motorspeed_right = speed_right

	def get_speed(self) -> float:
		"""Calcule la vitesse moyenne du robot
			
			Return:
				Retourne un float correspondant à la vitesse moyenne instantané du robot
		"""
		return (self._motorspeed_right + self._motorspeed_left) / 2
	
	def get_angular_speed(self) -> float:
		"""Calcule la vitesse angulaire (autrement dit, la vitesse de rotation du robot)

			Return:
				angular_speed (float): Vitesse angulaire en radian/seconde
		"""
		angular_speed = (self._motorspeed_right - self._motorspeed_left) / self._WHEELBASE
		return angular_speed
	
	def get_distance_traveled(self) -> None:
		"""Calcule la distance parcouru du robot

			Return:
				distance (float): Distance parcourue calculer depuis les deux dernières positions
		"""
		# On prends ls deux dernier élément de la liste
		x1, y1 = self._trail_position[-2]
		x2, y2 = self._trail_position[-1]

		# On détermine si le robot est en marche arriere
		minus = 1 if self.get_speed()>0 else -1

		# On calcule la distance qui sépare ces deux points
		self._distance_traveled += math.sqrt((x2 - x1)**2 + (y2 - y1)**2) * minus

	def get_position(self) -> tuple[float, float]:
		"""Renvoie la position courante

			Return:
				Un tuple correspondant à la position courante
		"""
		return (self._position_x, self._position_y)
	
	def get_last_position(self) -> tuple[float, float]:
		"""Renvoie la pénultième position enregistré

			Return:
				Un tuple correspondant à la pénultième position enregistrer
		"""
		return self._trail_position[len(self._trail_position)-2]
	
	def set_position(self, x: float, y: float) -> None:
		"""Positione le robot au coordonné indiqué

			Args:
				x (float): Nouvelle position x
				y (float): Nouvelle position y
		"""

		self._position_x = x
		self._position_y = y
	
	def get_corners(self) -> list[tuple[float,float]]:
		"""Renvoie les quatres points qui délimite l'armature du robot

			Return:
				corners: Liste de 4 points (dans le sens horaire) qui forme le rectangle représentant l'armature du robot
		"""
		# Récupération du point centrale du robot
		origin_x, origin_y = self.get_position()
		
		# On prend le vecteur directeur et un vecteur qui lui est perpendiculaire
		vect_dir_x, vect_dir_y = self.get_vector_dir()
		vect_per_x, vect_per_y = (	self._dim[1]/2 * math.cos(-self._total_theta+(math.pi/2)), 
									self._dim[1]/2 * math.sin(-self._total_theta+(math.pi/2)))
		
		# On additionne les vecteur entre eux pour obtenir les quatres points
		corner_upper_right = (	origin_x + vect_dir_x - vect_per_x,
								origin_y + vect_dir_y - vect_per_y)
		corner_upper_left = (	origin_x + vect_dir_x + vect_per_x, 
					   			origin_y + vect_dir_y + vect_per_y)
		corner_lower_right = (	origin_x - vect_dir_x + vect_per_x, 
								origin_y - vect_dir_y + vect_per_y)
		corner_lower_left = (	origin_x - vect_dir_x - vect_per_x, 
					   			origin_y - vect_dir_y - vect_per_y)

		# On regroupe le tout dans une liste
		corners = [corner_upper_left, corner_upper_right, corner_lower_left, corner_lower_right]
		return corners

	def reset(self):
		self._distance_traveled = 0

	def to_str(self):
		
		return f"\ntheta = {math.degrees(self._total_theta)}\nspeed left, right = {self._motorspeed_left},{self._motorspeed_right}\n_distance_traveled = {self._distance_traveled}\n"

# -ROBOT MOCKUP-------------------------------------------------------------------------------------------------
class RobotFake:
	"""Robot Fake simulant la future API du Robot2I013 
	"""

	WHEEL_BASE_WIDTH = 117  # distance (mm) de la roue gauche a la roue droite.
	WHEEL_DIAMETER = 66.5 #  diametre de la roue (mm)
	
	def __init__(self):
		"""Constructeur du robotFake simulant une api
		"""
		self.MOTOR_LEFT = 1
		self.MOTOR_RIGHT = 2

		self._recording = False

		self.offset_encoder_right = 0
		self.offset_encoder_left = 0

		self.motorspeed_right = 0
		self.motorspeed_left = 0

		pass
	
	
	# -METHODE-------------------------------------------------------------------------------------------------
	def set_motor_dps(self, port, dps) -> None:
		"""Mets a jour la vitesse à dps du robot selon le port (moreur droit ou gauche)
		"""
		
		# En fonction du port, on assigne le dps au bon moteur (ou les deux le cas échéant)
		if port == self.MOTOR_RIGHT:
			self.motorspeed_right = dps
		elif port == self.MOTOR_LEFT:
			self.motorspeed_left = dps
		elif port == (self.MOTOR_RIGHT + self.MOTOR_LEFT):
			self.motorspeed_right = dps
			self.motorspeed_left = dps

		#print(f"set_motor_dps : port = {port}, dps = {dps}")

	def offset_motor_encoder(self, port, offset) -> None:
		"""Simulation mise a jour offset
		"""

		# Modification de l'offset selon le port choisit
		if port == self.MOTOR_RIGHT:
			self.offset_encoder_right = offset
		elif port == self.MOTOR_LEFT:
			self.offset_encoder_left = offset
		elif port == (self.MOTOR_RIGHT + self.MOTOR_LEFT):
			self.offset_encoder_right = offset
			self.offset_encoder_left = offset

		#print(f"offset_motor_encoder : port = {port}, offset = {offset}")

	def get_motor_position(self) -> tuple[float,float]:
		"""Simulation de récuperation de la position des moteurs
		"""
		return self.offset_encoder_left + self.motorspeed_left, self.offset_encoder_right + self.motorspeed_right
	
	def _start_recording(self) -> None:
		"""Boucle infinie pour simuler la 
		"""
		while self._recording:
			print("Caméra active")
			time.sleep(1/25) # -> Simule le frame par sec de la caméra
		
	def start_recording(self) -> None:
		"""Simule démarrage de la caméra
		"""
		print("Record begin")
		self._recording = True
		self._thread = threading.Thread(target=self._start_recording)
		self._thread.start()

	def _stop_recording(self) -> None:
		"""Simule l'arrete de la caméra
		"""
		print("Record stop")
		self._recording = False
		self._thread.join()
		self._thread = None

	def servo_rotate(self,positon):
		pass

	def get_image(self):
		"""Simule un renvoie d'image. pioche au hazard dans le dossier ressource_photo
		"""
		path = "./src/model/ressource_photo/"
		return path + random.sample(os.listdir(path), 1)[0]
		
	def get_distance(self):
		return random.randint(0,100)
		
# -APDATER PATTERN-------------------------------------------------------------------------------------------------
class RobotAdapter:
	"""Adapte les fonctions du robot simulé Robot() pour un robot du type RoboFake()

		Attributes:
			_robot (Robot): Correspond à l'API du véritable robot (ici, on utilisera un robotFake ou la véritable API)
			_total_theta (int | float): Angle totale parcouru par le robot (en rapport avec le plan)
			_last_update (int | float): Temps de la dernière update effectué par le robot
	"""

	def __init__(self, robotfake: RobotFake, theta: float = 0.0) -> None:
		"""Constructeur d'un adaptateur

			Petite précision : 
				L'angle theta est ajouter comme attribut car l'API n'enregistre pas d'angle
				Une variable `last_update` aussi est ajouté pour conserver en mémoire le dernier appel
		"""

		self._robot = robotfake
		self._total_theta = theta
		self._last_update = 0
		self.offset_encoder_right = 0
		self.offset_encoder_left = 0
		self._distance_traveled = 0
		self._captor_theta = 0
		self._beacon_in_sight = False

	#- METHODE-------------------------------------------------------------------------------------------------
	def set_speed(self, speed_left: float = 0.0, speed_right: float = 0.0) -> None:
		"""Mise a jour de la vitesse des moteurs

			Adapte la fonction set_speed du robot simulé

			Args:
				speed_left (float): Vitesses du moteur gauche
				speed_right (float): Vitesses du moteur droit
		"""
		# Si les moteurs doivent avoir la même vitesse, on assigne le dps en 1 seule commande, sinon de façon séparé
		if speed_left == speed_right:
			self._robot.set_motor_dps(self._robot.MOTOR_LEFT + self._robot.MOTOR_RIGHT, speed_left)
		else:
			self._robot.set_motor_dps(self._robot.MOTOR_LEFT, speed_left)
			self._robot.set_motor_dps(self._robot.MOTOR_RIGHT, speed_right)

	def get_distance_traveled(self) -> None:
		"""Renvoie la distance parcourue du robot

			Récupère la distance parcourue du robot en calculant la distance avec décalage entre les offsets, puis renvoie la moyenne des deux pour avoir la distance moyenne parcourue

			Return:
				distance_traveled (float): Moyenne correspondant à la distance parcourue par le robot
		"""
		# On récupère la position des moteurs
		angle_left, angle_right = self._robot.get_motor_position()
		print(f"Angle recupérer : {angle_left}, {angle_right}")
		

		# On calcule la distance parcourue selon l'angle effectuer en soustrayant l'offset multiplier par le rayon
		# Voir page 10 du lien : https://ena.etsmtl.ca/pluginfile.php/650822/mod_resource/content/0/PHYchap6.pdf
		distance_left = (angle_left - self.offset_encoder_left) * (self._robot.WHEEL_DIAMETER*math.pi/360) 
		distance_right = (angle_right - self.offset_encoder_right) * (self._robot.WHEEL_DIAMETER*math.pi/360)

		# Calcule de la moyenne parcourue
		distance_traveled = (distance_left + distance_right)/2
		print(f"Distance parcourue = {distance_traveled}")
		
		#décommenter le `+` pour la ver irl, ajouter `+` pour la version mock
		self._distance_traveled += distance_traveled
	
	def reset(self):
		# On récupère la position des deux moteurs
		new_offset_left, new_offset_right  = self._robot.get_motor_position()
		print(f"Angle recupérer lors du reset : {new_offset_left}, {new_offset_right}")

		self.offset_encoder_left = new_offset_left
		self.offset_encoder_right = new_offset_right

		# On met à jour l'offset des moteurs pour les nouveaux calcule de distance
		self._robot.offset_motor_encoder(self._robot.MOTOR_LEFT,new_offset_left)
		self._robot.offset_motor_encoder(self._robot.MOTOR_RIGHT,new_offset_right)

		self._distance_traveled = 0
		self._total_theta = 0
		

	
	def get_angle(self):
		# On récupère la position des moteurs
		angle_left, angle_right = self._robot.get_motor_position()
		print(f"Angle de l'Offset : {self.offset_encoder_left}, {self.offset_encoder_right}")
		print(f"Angle de courant : {angle_left}, {angle_right}")

		distance_left = (angle_left - self.offset_encoder_left) * (self._robot.WHEEL_DIAMETER*math.pi/360) 
		distance_right = (angle_right - self.offset_encoder_right) * (self._robot.WHEEL_DIAMETER*math.pi/360)
		
		#décommenter le `+` pour la ver irl, ajouter `+` pour la version mock
		self._total_theta += (distance_right - distance_left) / self._robot.WHEEL_BASE_WIDTH

	def servo_rotate(self, position) -> None:
		"""Place la caméra à l'angle (degrée) voulue (entre -90 et 90)
		"""
		self._captor_theta += position
		position += 90
		self._robot.servo_rotate(position)

	def start_recording(self) -> None:
		"""Demarre le record
		"""
		self._robot.start_recording()

	def stop_recording(self) -> None:
		"""Stop le record
		"""
		self._robot._stop_recording()

	def get_image(self):
		"""Renvoie une image
		"""
		return self._robot.get_image()

	def get_distance(self):
		return self._robot.get_distance()

	def get_position(self) -> tuple[int, int]:
		"""Renvoie une position unique (figuration)
		"""
		pass
	
	def update_position(self) -> None:
		"""Mise à jour de la position du robot
		"""
		pass
	
	def search_balise_color(self, balise_color, image):

		#bgr to hsv
		hsv_image  = cv.cvtColor(image,cv.COLOR_BGR2HSV)

		
		all_mask = {}
		contours = {}
		clean_contours = []
		apparent_color = []
		
		for color in balise_color: 
			lower_limit, upper_limit = self.get_limits(color)
			all_mask[color] = cv.inRange(hsv_image, lower_limit, upper_limit)
		
			#plt.figure(figsize=[10,10])
			#plt.imshow(all_mask[color]);plt.title(color)

		for color,mask in all_mask.items():
			contours[color], _= cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

			#image_copy = image.copy()

			# voir : https://pyimagesearch.com/2021/10/06/opencv-contour-approximation/
			for elem in contours[color]:
				ep = 0.05 * cv.arcLength(elem, True)
				approx = cv.approxPolyDP(elem, ep, True)
				
				#On essaie de retirer un maximum de bruit
				if len(approx) == 4:
					clean_contours.append(approx)
					apparent_color.append(color)
					#cv.drawContours(image_copy, [approx], -1, (0,255,255), 3)
			

			# Spawn a new figure
			#plt.figure(figsize=[10,10])
			#plt.imshow(image_copy[:,:,::-1])
			# Turn off axis numbering
			#plt.axis('off')
		
		try:
			min_x = min([rect[0][0][0] for rect in clean_contours])
			max_x = max([rect[2][0][0] for rect in clean_contours])
			min_y = min([rect[0][0][1] for rect in clean_contours])
			max_y = max([rect[2][0][1] for rect in clean_contours])
		except:
			return False

		return max_x - min_x > 0 and max_y - min_y > 0 and set(apparent_color) == set(balise_color)


	
	def get_limits(self,color):
		"""Donne les nuances max et min de la couleur en paramètre
		"""

		if "blue" == color:
			lower_limit = np.array([100,84,46])
			upper_limit = np.array([110,255,255])
		if "red" == color:
			lower_limit = np.array([0,150,100])
			upper_limit = np.array([10,255,255])
		if "green" == color:
			lower_limit = np.array([59,57,57])
			upper_limit = np.array([70,255,255])
		if "yellow" == color:
			lower_limit = np.array([20,128,93])
			upper_limit = np.array([39,255,255])
		if "white" == color:
			lower_limit = np.array([3,26,99])
			upper_limit = np.array([36,71,165])

		return lower_limit, upper_limit
	
	
	def to_str(self):
		
		return f"\ntheta = {math.degrees(self._total_theta)}\nlast_update = {self._last_update}\noffset right, left = {self.offset_encoder_right}, {self.offset_encoder_left}\n_distance_traveled = {self._distance_traveled}\n"


