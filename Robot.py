from Moteur import Moteur
class Robot :
	"""
		Modélisation d'un robot de Sorbonne Université
	"""

	def __init__(self, width, length, x:float=0, y:float=0) -> None:
		
		self._dim = (width, length)
		
		#Position en x et y du centre du robot 
		self.posx = x
		self.posy = y
		
		#Position globale du robot (devant, derriere, droit et gauche)
		self.posFront = (x, y + length/2)
		self.posRear = (x, y - length/2)
		self.posLeftSide = (x - (width/2), y)
		self.posRightSide = (x + (width/2), y)

		#Ajout des Moteurs au robot (droite et gauche)
		self._motorRight = Moteur("droit")
		self._motorLeft = Moteur("gauche")

	
	def rotate(self) :
		""" 
			Tourne le robot de 90 degree vers la droite
		"""

		#Init biais
		biasX = 0
		biasY = 0

		if (self.posx, self.posy) != (0,0) :
			biasX = self.posx
			biasY = self.posx
		
		# Translation vers le centre
		pfront = (self.posFront[0] + biasX, self.posFront[1] + biasY)
		prear  = (self.posRear[0] + biasX, self.posRear[1] + biasY)
		plside = (self.posLeftSide[0] + biasX, self.posLeftSide[1] + biasY)
		prside = (self.posRightSide[0] + biasX, self.posRightSide[1] + biasY)

		#Rotation
		pfront = (-1*pfront[1], pfront[0])
		prear  = (-1*prear[1], prear[0])
		plside = (-1*plside[1], plside[0])
		prside = (-1*prside[1], prside[0])

		# Translation vers le point de départ
		self.posFront = (pfront[0] + (-1*biasX), pfront[1] + (-1*biasY))
		self.posRear = (prear[0] + (-1*biasX), prear[1] + (-1*biasY))
		self.posLeftSide = (plside[0] + (-1*biasX), plside[1] + (-1*biasY))
		self.posRightSide = (prside[0] + (-1*biasX), prside[1] + (-1*biasY))





	
	
