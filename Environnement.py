class Environnement :
	"""
	Classe définissant un environnement de simulation virtuel pour la manipulation d'un agent (robot)
	"""

	def __init__(self, x, y, agent, clockPace = 1) -> None:
		"""
			Constructeur de la classe Environnement.
			arg x : taille max de l'abscisse du rectangle
			arg y : taille max de l'ordonnée du rectangle
			arg clockPace : Pas de temps de l'environnement

			---

			Attribut d'instance env. :
			onGoing 			-> boolean qui dit si oui on non la simulation est en cours
			currentClock 		-> variable qui retient le temps courant
			clockPace			-> Increment de temps de la simulation
			maxReachablePoint 	-> Définition de l'aire de simulation par le point maximal (diagonale au centre)
		"""
		
		self.onGoing = False
		self.currentClock = 0
		self.clockPace = clockPace
		self.maxReachablePoint = (x,y)
		self.agent = agent



	def isOut(self) :
		if self.agent.posCenter[0]<0  or self.agent.posCenter[0] > self.maxReachablePoint[0] or self.agent.posCenter[1]<0  or self.agent.posCenter[0] > self.maxReachablePoint[1] :
			print("l'agent est en dehors de la zone de test")
			return 1


	def clockCount(self) :
		"""
			Générateur de temps qui incrémente self.currentClock de self.clockPace à chaque appel
		"""
		while self.onGoing :
			self.currentClock += self.clockPace
			yield self.currentClock
	
	def runEnv(self):
		"""
			Active l'Environnement en passant l'attribut onGoing True 
		"""
		if self.onGoing :
			print("L'environnement est déjà en cours d'éxécution")
		else :
			self.onGoing = True

		
	
	
	def stopEnv(self):
		"""
			Arrête l'Environnement en passant l'attribut onGoing à False
		"""
		if not self.onGoing :
			print("L'environnement est déjà arrêté")
		else :
			self.onGoing = False
