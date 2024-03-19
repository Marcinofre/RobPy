from utils.vecteur import Vecteur
import os
import math

class Capteur :
    """
		Modélisation du capteur de mouvement du robot
	"""

    def __init__(self, vecteurDirecteurRobot:Vecteur) -> None:
        """
			Attributes:

				ray: Vecteur représentant le rayon unitaire du capteur (de même orientation et direction que le vecteurDirecteur du robot)
				vision: Portée maximale de la vision du capteur
				touchObstacle: Etat du rayon qui indique s'il croise un obstacle

			Args:
				vecteurDirecteurRobot: Vecteur directeur du robot sur lequel repose le capteur
				
	    """
        self.ray = self.treatVector(vecteurDirecteurRobot)
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

       

class Robot :
	"""
		Modélisation d'un robot de Sorbonne Université
	"""

	def __init__(self, width:int, length:int, x:float=0, y:float=0, vecteurDirecteur = Vecteur(0,-1)):
		"""Constructeur de la classe Robot
			
			Args:
				width : Largeur du robot
				length : Longueur du robot
				x: Position en x du centre du robot
				y: Position en y du centre du robot
			
			Attributes:
				dim: Dimension du robot défini par sa largeur et sa longueur
				MoteurD: Scalaire vitesse du moteur droit du robot
				MoteurG: Scalaire vitesse du moteur gauche du robot
				rayon: Empatement entre les deux roue/moteur 
				isActive: Booléen qui définit si le robot est allumé ou non
				vectD: Vecteur direction du robot
				posCenter: Position du centre au départ de la simulation du robot défini par x et y (initialisé à 0,0)
				capteur: Capteur d'obstacle du robot
				loin: Booléen qui exprime si l'obstacle est loin ou non
				isControlled: Booléen qui status si le robot est controlé par un controleur ou non
				trace: Tableau de tuple qui comprend toutes les positions que prend le robot durant la simulation

			
		"""
		
		self._dim = (width, length)

		self.MoteurD = 0.0

		self.MoteurG = 0.0

		self.rayon = 1 					# rayon du cercle passant par les deux roues en mètres, à définir, 0.25 n'est qu'une valeur abstraite

		self.isActive = 1
		
		self.vectD = vecteurDirecteur 	# Vecteur direction
	
		self.posCenter = (x,y)			# Position en x et y du centre du robot
		
		self.rotation = self.vectD.calculerAngle(Vecteur(0,-1))

		self.loin = True

		self.isControlled = False

		self.capteur = Capteur(vecteurDirecteur) 		# Ajout d'un capteur pour le Robot
 
		self.trace=[self.posCenter] 					# enregister la position

	def VitesseAngulaire(self) :
		"""Permet de faire tourner le vecteur direction quand une roue va plus vite que l'autre.

			Returns:
				Retourne l'angle de rotation a effectuer en prenant en compte la vitesse entre les deux moteurs
		"""
		# 1er Cas : La roue droite est plus rapide, l'angle est positif, le robot tourne à gauche.
		# 2ème Cas : La roue gauche est plus rapide, l'angle est négatif, le robot tourne à droite.
		# 3ème Cas : Les deux roues ont la même vitesse, l'angle est nul, le robot ne tourne pas.
		diff = self.MoteurD - self.MoteurG 
		angle = diff / self.rayon
		angle = angle * (180/math.pi)
		return round(angle,5)

	def calcVitesseMoyenne(self) :
		"""Calcule la vitesse moyenne du Robot en fonction de la vitesse des ses moteurs

			Returns:
				Retourne la vitesse moyenne du robot
		"""
		return round((self.MoteurD + self.MoteurG)/2,2)

	def avancerRobot(self):
		"""Calcul la position du robot en le faisant avancer en fonction de la vitesse et du vecteur direction
		"""
		vit = self.calcVitesseMoyenne()
		self.posCenter = (	round(self.posCenter[0] + (self.vectD.x * vit), 1),
							round(self.posCenter[1] + (self.vectD.y * vit), 1))

	def setVitesseRoue(self, d:"int | float", g:"int | float"):
		"""Définit les vitesses des moteurs

			Args:
				d: Vitesse du moteur droit
				g: Vitesse du moteur gauche
        """
		self.MoteurD = d
		self.MoteurG = g

	def rotateAllVect(self, angle):
		"""Rotation en degré du vecteur directeur et du vecteur unitaire du capteur du robot

			Args:
				angle: Angle de rotation à appliquer en degré
		"""
		self.vectD.rotationAngle(angle)
		self.capteur.ray.rotationAngle(angle)
		self.rotation += angle

	def getCarcasse(self) -> list[tuple["int|float", "int|float"]]: 
		"""Calcule les coordonnées des 4 points du robot en fonction de l'angle du robot

			Returns:
				Une liste de tuple correspondant au quatre point de l'armature du robot
		"""
		larg = self._dim[0]/2
		long = self._dim[1]/2

		x = self.posCenter[0]
		y = self.posCenter[1]

		TRC_V = Vecteur(+larg, -long)
		TLC_V = Vecteur(+larg, +long)
		BRC_V = Vecteur(-larg, -long)
		BLC_V = Vecteur(-larg, +long)
		
		if self.rotation!=0 :
			TRC_V.rotationAngle(self.rotation)
			TLC_V.rotationAngle(self.rotation)
			BRC_V.rotationAngle(self.rotation)
			BLC_V.rotationAngle(self.rotation)
		
		TRC_T = (TRC_V.x + x,TRC_V.y + y)
		TLC_T = (TLC_V.x + x,TLC_V.y + y)
		BRC_T = (BRC_V.x + x,BRC_V.y + y)
		BLC_T = (BLC_V.x + x,BLC_V.y + y)
		

		return [TRC_T,TLC_T,BLC_T,BRC_T]

	def getRay(self, distance):
		"""Récupère le rayon projeté, puis le translate vers le centre du robot
			
			Args:
				distance: Distance de projection du vecteur

			Returns:
				Un vecteur 

		"""
		vecteurRayon = self.capteur.projectionRay(distance)
		return Vecteur(vecteurRayon[0],vecteurRayon[1])
	
	def getForInterfaceRay(self):
		return self.capteur.interfaceRay
	
	def update(self):
		self.rotateAllVect(self.VitesseAngulaire())
		self.avancerRobot()
		
		#enregister chaque update 
		self.update_trace()
	

	def getRectangle(self):
		"""Permet d'obtenir les lignes représentant les 4 côtés du rectangle

			Returns:
				???
		"""
		coins = self.getCarcasse()

		haut = ((coins[1]),(coins[0]))
		bas = ((coins[2]),(coins[3]))
		gauche = ((coins[1]),(coins[3]))
		droit = ((coins[0]),(coins[3]))
		return [haut,bas,gauche,droit]
	

	def update_trace(self):
		"""Met à jour la trace en ajoutant la nouvelle position à l'attribut `trace`
		"""
		if not self.trace or (self.trace[-1]!=self.posCenter):
			self.trace.append(self.posCenter)

