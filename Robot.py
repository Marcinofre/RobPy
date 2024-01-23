from Moteur import Moteur
class Robot :
	"""
		Modélisation d'un robot de Sorbonne Université
	"""

	def __init__(self, width, length, x:float=0, y:float=0) -> None:
		
		self._dim = (width, length)
		
		#Position en x et y du centre du robot 
		self.posCenter = (x,y)
		
		#Position globale du robot (devant, derriere, droit et gauche)
		self.posFront = (x, y + length/2)
		self.posRear = (x, y - length/2)
		self.posLeftSide = (x - (width/2), y)
		self.posRightSide = (x + (width/2), y)

		#Vitesse du Robot (x, y)
		self.vectV = (1,1)

		#Ajout des Moteurs au robot (droite et gauche)
		self._motorRight = Moteur("droit")
		self._motorLeft = Moteur("gauche")

		
	def allPos(self) :
		"""
			Print l'ensemble des positions disponible du robot
		"""
		print(f"Position du robot : {self.posCenter}")
		#print(f"position Avant : {self.posFront}")
		#print(f"position Arrière : {self.posRear}")
		#print(f"position Coté gauche : {self.posLeftSide}")
		#print(f"position Coté droit : {self.posRightSide}")

	def runRobot(self) :
		"""
			Fais rouler le robot tout droit
		"""
		self.posCenter = (self.posCenter[0] + self.vectV[0], self.posCenter[1] + self.vectV[1])




	








	
	
