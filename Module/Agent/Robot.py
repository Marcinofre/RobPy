from Module.Vecteur import Vecteur
import os
import math
from Module.Agent.Moteur import Moteur
from Module.Agent.Capteur import Capteur

class Robot :
	"""
		Modélisation d'un robot de Sorbonne Université
	"""

	def __init__(self, width:int, length:int, x:float=0, y:float=0, vecteurDirecteur = Vecteur(0,-10)):
		"""
			Constructeur de la classe Robot :
			arg width : Largeur du robot
			arg length : Longueur du robot

			---

			Attribut d'instance env. :
			dim				-> Dimension du robot défini par sa largeur et sa longueur
			isActive		-> Booléen qui définit si le robot est allumé ou non
			vitesseMoyenne	-> Scalaire définissant la vitesse du robot
			vectD 	        -> Vecteur direction du mouvement du robot
			posCenter       -> Position du centre du robot dans l'environnement défini par x et y (initialisé à 0,0)
			Capteur			-> Capteur d'obstacle du robot
		"""
		
		self._dim = (width, length)

		self.MoteurD = Moteur("Droit") 	# Moteur de la roue droite

		self.MoteurG = Moteur("Gauche") # Moteur de la roue gauche

		self.rayon = 1 					# rayon du cercle passant par les deux roues en mètres, à définir, 0.25 n'est qu'une valeur abstraite

		self.isActive = 1
		
		self.vectD = vecteurDirecteur 	# Vecteur direction
        
		self.vitesseMoyenne = 0
	
		self.posCenter = (x,y)			# Position en x et y du centre du robot
		
		self.rotation = 0

		self.loin = True

		self.isControlled = False

		self.capteur = Capteur(vecteurDirecteur) 		# Ajout d'un capteur pour le Robot

		# ici 
		self.trace=[self.posCenter] # enregister la position

	def VitesseAngulaire(self) :
		"""
			Permet de faire tourner le vecteur direction quand une roue va plus vite que l'autre.
		"""
		# 1er Cas : La roue droite est plus rapide, l'angle est positif, le robot tourne à gauche.
		# 2ème Cas : La roue gauche est plus rapide, l'angle est négatif, le robot tourne à droite.
		# 3ème Cas : Les deux roues ont la même vitesse, l'angle est nul, le robot ne tourne pas.
		diff = self.MoteurD.vitesseMoteur - self.MoteurG.vitesseMoteur 
		angle = diff / self.rayon
		pi = math.pi
		angle = angle * (180/pi)
		return round(angle,5)

	def calcVitesseMoyenne(self) :
		"""
			Calcule la vitesse moyenne du Robot en fonction de la vitesse des ses moteurs
		"""
		self.vitesseMoyenne = round((self.MoteurD.vitesseMoteur*self.MoteurD.state + self.MoteurG.vitesseMoteur*self.MoteurG.state)/2,2)

	def avancerRobot(self):
		"""
			Met à jour la position du robot en le faisant avancer en fonction de la vitesse et du vecteur direction
		"""
		self.calcVitesseMoyenne()
		print(self.vitesseMoyenne)
		self.posCenter = (round(self.posCenter[0] + (self.vectD.x * self.vitesseMoyenne), 1),
						round(self.posCenter[1] + (self.vectD.y * self.vitesseMoyenne), 1))

	def setVitesseRoue(self, d, g):
		"""
			Définit la vitesse des deux roue du robot
		"""
		self.MoteurD.vitesseMoteur = d
		self.MoteurG.vitesseMoteur = g

	def rotateAllVect(self, angle) :
		"""
			Rotation en degré du robot, ce qui demande une rotation du vecteur directeur et du vecteur representé par les 4 coins du robot
		"""
		self.vectD.rotationAngle(angle)
		self.capteur.ray.rotationAngle(angle)
		self.rotation += angle
		print(self.rotation)

	def getCarcasse(self):
		"""
			Renvoie les coordonnées des 4 points du robot sous la forme de Liste de Tuple
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
		"""
			Récupère le rayon projeté, puis le translate vers le centre du robot
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
		"""
			Permet d'obtenir les lignes représentant les 4 côtés du rectangle
		"""
		coins = self.getCarcasse()

		haut = ((coins[1]),(coins[0]))
		bas = ((coins[2]),(coins[3]))
		gauche = ((coins[1]),(coins[3]))
		droit = ((coins[0]),(coins[3]))
		return [haut,bas,gauche,droit]
	
	#test ici
	def update_trace(self):
		if not self.trace or (self.trace[-1]!=self.posCenter):
			self.trace.append(self.posCenter)