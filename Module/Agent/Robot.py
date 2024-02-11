from Module.Vecteur import Vecteur
import os
import math
from Module.Agent.Moteur import Moteur

class Robot :
	"""
		Modélisation d'un robot de Sorbonne Université
	"""

	def __init__(self, width:int, length:int, x:float=0, y:float=0) -> None:
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
		"""
		
		self._dim = (width, length)

		self.MoteurD = Moteur("Droit") # Moteur de la roue droite

		self.MoteurG = Moteur("Gauche") # Moteur de la roue gauche

		self.Rayon = width/2 # Rayon du cercle passant par les deux roues en mètres, à définir, 0.25 n'est qu'une valeur abstraite

		self.isActive = 0
		
		self.vectD = Vecteur(0, 0)  # Vecteur direction, par défaut (0, 0) => représente les deux roues
        
		self.vitesseMoyenne = 0
	
		self.posCenter = (x,y)	# Position en x et y du centre du robot
		
		self.rotation = 0

	def VitesseAngulaire(self) :
		"""
			Permet de faire tourner le vecteur direction quand une roue va plus vite que l'autre.
		"""
		# 1er Cas : La roue droite est plus rapide, l'angle est positif, le robot tourne à gauche.
		# 2ème Cas : La roue gauche est plus rapide, l'angle est négatif, le robot tourne à droite.
		# 3ème Cas : Les deux roues ont la même vitesse, l'angle est nul, le robot ne tourne pas.
		diff = self.MoteurD.vitesseMoteur - self.MoteurG.vitesseMoteur 
		angle = diff / self.Rayon
		pi = math.pi
		angle = angle * ( 180/pi )
		self.rotateAllVect(angle)

	def calcVitesseMoyenne(self) :
		"""
			Calcule la vitesse moyenne du Robot en fonction de la vitesse des ses moteurs
		"""
		self.vitesseMoyenne = round((self.MoteurD.vitesseMoteur*self.MoteurD.state + self.MoteurG.vitesseMoteur*self.MoteurG.state)/2,2)

	def avancerRobot(self):
		"""
			Met à jour la position du robot en le faisant avancer en fonction de la vitesse et du vecteur direction
		"""
		if (not self.MoteurD.state) and (not self.MoteurG.state):
			return
		else :
			self.VitesseAngulaire()
			self.posCenter = (round(self.posCenter[0] + (self.vectD.x * self.vitesseMoyenne), 1),
					 		  round(self.posCenter[1] + (self.vectD.y * self.vitesseMoyenne), 1))
    
	
	def rotateAllVect(self, angle) :
		"""
			Rotation en degré du robot, ce qui demande une rotation du vecteur directeur et du vecteur representé par les 4 coins du robot
		"""
		self.vectD.rotationAngle(angle)
		self.rotation = angle

	def getCarcasse(self):
		"""
			Renvoie les coordonnées des 4 points du robot sous la forme de Liste de Tuple
		"""
		larg = self._dim[0]/2
		long = self._dim[1]/2

		TRC = (self.posCenter[0]+larg, self.posCenter[1]-long)
		TLC = (self.posCenter[0]+larg, self.posCenter[1]+long)
		BRC = (self.posCenter[0]-larg, self.posCenter[1]-long)
		BLC = (self.posCenter[0]-larg, self.posCenter[1]+long)
		
		if self.rotation!=0 :
			rad = math.radians(self.rotation)
			TRC = (round(TRC[0]*math.cos(rad) - TRC[1]*math.sin(rad),1),
		  		  round(TRC[0]*math.sin(rad) + TRC[1]*math.cos(rad),1))
			TLC = (round(TLC[0]*math.cos(rad) - TLC[1]*math.sin(rad),1),
		  		  round(TLC[0]*math.sin(rad) + TLC[1]*math.cos(rad),1))
			BRC = (round(BRC[0]*math.cos(rad) - BRC[1]*math.sin(rad),1),
		  		  round(BRC[0]*math.sin(rad) + BRC[1]*math.cos(rad),1))
			BLC = (round(BLC[0]*math.cos(rad) - BLC[1]*math.sin(rad),1),
		  		  round(BLC[0]*math.sin(rad) + BLC[1]*math.cos(rad),1))

		return [TRC,TLC,BRC,BLC]


 
 





	
	
