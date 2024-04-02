from simpack.utils.vecteur import Vecteur
import time
import math

class Capteur :
    """
		Modélisation du capteur de mouvement du robot
	"""

    def __init__(self, vecteurDirecteurRobot: Vecteur) -> None:
        """
		Attributes:

			ray: Vecteur représentant le rayon unitaire du capteur (de même orientation et direction que le vecteurDirecteur du robot)
			vision: Portée maximale de la vision du capteur
			touchObstacle: Etat du rayon qui indique s'il croise un obstacle

		Args:
		vecteurDirecteurRobot: Vecteur directeur du robot sur lequel repose le capteur
		"""
        self.ray = self.treatVector(vecteurDirecteurRobot)
        self.initial_ray = self.ray
        self.vision = 500
        self.interfaceRay = self.ray
        self.touchObstacle = False
        self.distanceObstacle = 0


    def projectionRay(self,distance):
        """
            Retourne le rayon projeté à la distance passé en paramètre en mètres
        """
        return (self.ray.x * distance, self.ray.y * distance)
    
    def treatVector(self, vec : Vecteur):
        res = Vecteur(0,0)
        if vec.y > 0 :
            res.y = 1
        if vec.x > 0 :
            res.x = 1
        if vec.x<0 :
            res.x = -1
        if vec.y<0 :
            res.y = -1
        return res

       

"""
	Class définissant le robot, le robotFake et son adaptateur qui sera utiliser dans l'environnement de simulation
"""

#----Import zone-----------------------------------
import math
import time
#--------------------------------------------------


#----ROBOT------------------------------------------
class Robot:
	"""Class Robot qui définit un robot de licence d'Informatique de Sorbonne Université

		Attributes:
			_dim (tuple[int,int]): Dimension du robot longueur, largeur
			_wheelbase (int): Empatement entre les deux roues

			_position_x (float): Position courante du robot sur l'abcisse dans l'environnement virtuelle
			_position_y (float): Position courante du robot sur l'ordonnée dans l'environnement virtuelle
			_total_theta (float): Angle de rotation vis-à-vis du plan de l'environnement
			_captor_theta (float): Angle de rotation du capteur vis-à-vis du plan du vecteur directeur


			_motorspeed_right (float): Vitesse du moteur droit
			_motorspeed_left (float): Vitesse du moteur gauche

			_trail_position (list[tuple[float, float]]): Tableau enregistrant toutes les positions du robot précédente
			_last_update (float): Temps de la dernière mise à jour effectué

	"""
	
	
	
	#-CONSTRUCTEUR-------------------------------------------------------------------------------------------------
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

	
	
	
	#-METHODE-------------------------------------------------------------------------------------------------
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
	
	def get_distance_traveled(self) -> float:
		"""Calcule la distance parcouru du robot

			Return:
				distance (float): Distance parcourue calculer depuis les deux dernières positions
		"""
		# On prends ls deux dernier élément de la liste
		x1, y1 = self._trail_position[-2]
		x2, y2 = self._trail_position[-1]

		# On calcule la distance qui sépare ces deux points
		distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

		return distance

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