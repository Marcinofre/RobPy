
from Module.Env.Obstacle import Obstacle
from Module.Agent.Robot import Robot
from Module.Vecteur import Vecteur

class Environnement() :
	"""
	Classe définissant un environnement de simulation virtuel pour la manipulation d'un agent (robot)
	"""

	def __init__(self, x, y, agent:Robot) -> None:
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
			setObstacle	        -> Un ensemble contenant tous les obstacles de l'environnement
		"""

		self.currentClock = 0
		self.clockPace = 1
		self.gentime = None
		self.maxTime = 10000
		self.maxReachablePoint = (x,y)
		self.isRunning = False
		
		self.agent = agent
		self.setObstacle = set()
		self.addObstacle((Obstacle(0,0,x,y)))

		self.bordure_haut 	= ((0,0),(x,0))
		self.bordure_droite 	= ((x,0),(x,y))
		self.bordure_gauche 	= ((0,0),(0,y))
		self.bordure_bas 	= ((0,y),(x,y))



	def isOut(self) :
		if self.agent.posCenter[0]<0  or self.agent.posCenter[0] > self.maxReachablePoint[0] or self.agent.posCenter[1]<0  or self.agent.posCenter[0] > self.maxReachablePoint[1] :
			print("l'agent est en dehors de la zone de test")
			return 1

	def clockCount(self) :
		"""
			Générateur de temps qui incrémente self.currentClock de self.clockPace à chaque appel
		"""
		while True:
			self.currentClock += self.clockPace
			yield self.currentClock
	
	def initSimulation(self):
		"""
			Initialisation des variable de l'environnement pour la simulation
		"""
		#Initialise le générateur
		self.gentime = self.clockCount()
		#Initialise à True isRunning pour l'updater dans le main
		self.isRunning = True
		#reset le currentClock
		self.currentClock = 0
		
	def run(self):
		try :
			print(next(self.gentime))
		except:
			print("Fin du compteur")
			return

	def addObstacle(self, obs) :
		"""
			Prend en argument obs soit une List soit un objet de la classe Obstacle :
				- Si c'est un objet de la classe Obstacle, il est ajouté au setObstacle.
				- Si c'est une List, il parcourt la liste et chaque élément de la classe Obstacle est ajouté au setObstacle.
				- Si c'est ni l'un ni l'autre, on affiche : L'élément n'est pas un obstacle.
		"""
		if isinstance(obs, list):
			for obj in obs :
				if isinstance(obj, Obstacle) :
					self.setObstacle.add(obj)
		elif isinstance(obs, Obstacle):
				self.setObstacle.add(obs)
		else :
			print("L'élément n'est pas un obstacle")

	def doesCollide(self):
		"""
        	Détermine si rob est en collision avec obs, renvoie True ou False. 
			Fait un produit de produit vectoriel de la forme (AB ^ AC)(AB ^ AD) ET (CD ^ CA)(CD ^ CB)
        """
		for i in self.setObstacle:
			AB = self.agent.vectD
			AC = self.creerVecteur((self.agent.posCenter[0], self.agent.posCenter[1]), (i.x0, i.y0))
			AD = self.creerVecteur((self.agent.posCenter[0], self.agent.posCenter[1]), (i.x1, i.y1))
			CA = self.creerVecteur((i.x0, i.y0), (self.agent.posCenter[0], self.agent.posCenter[1]))
			CB = self.creerVecteur((i.x0, i.y0), (self.agent.posCenter[0]+self.agent.vectD.x, self.agent.posCenter[1]+self.agent.vectD.y))
			CD = self.creerVecteur((i.x0, i.y0), (i.x1, i.y1))
			if (AB.produitVectoriel(AC)*AB.produitVectoriel(AD))<0 and (CD.produitVectoriel(CA)*CD.produitVectoriel(CB))<0 :
				return True
		return False
	
	def doesRayCollide(self):
		"""
			Calcule de la collision entre le rayon du capteur et de la bordure haute
		"""
		(x1, y1) = self.agent.posCenter
		(x2, y2) = self.agent.capteur.interfaceRay.toTuple()
		(x2,y2) = (x2+x1, y1+y2)			
		(x3, y3) = self.bordure_haut[0]
		(x4, y4) = self.bordure_haut[1]

		intersec1 = (x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)
		intersec2 = (x4 - x1) * (y2 - y1) - (y4 - y1) * (x2 - x1)
		intersec3 = (x1 - x3) * (y4 - y3) - (y1 - y3) * (x4 - x3)
		intersec4 = (x2 - x3) * (y4 - y3) - (y2 - y3) * (x4 - x3)
		

		self.agent.capteur.touchObstacle = (intersec1 * intersec2 < 0) and (intersec3 * intersec4 < 0)

	def retourCapteur(self, pas_distance):
		"""
			Simule la réponse que reçoit le capteur si son ray rencontre un objet
		"""
		distance_vue = 0
		vision = self.agent.capteur.vision

		# On projete le rayon si distance_vue est inférieur à la vision
		while (not self.agent.capteur.touchObstacle) and distance_vue < vision:
			
			distance_vue += pas_distance														#---> Incrementation de la distance
			self.agent.capteur.interfaceRay = self.agent.getRay(distance_vue)					#---> Récupère le rayon projeté à x distance
			self.doesRayCollide()																#---> Regarde si le rayon coupe un vecteur
			self.agent.capteur.distanceObstacle = self.agent.getRay(distance_vue).calcNorm()	#---> Calcul de la distance entre le robot est l'obstacle
		print(f'je regarde à {self.agent.capteur.distanceObstacle}')
		return True

	def update(self):
		print("UPDATE")
		if self.doesCollide():
			print("En collision!")
			return
		self.run()
		self.agent.update()


	def creerVecteur(self,coord1, coord2) :
			"""
				Prend les coordonnés des points A et B et retournent le vecteur AB
			"""
			return Vecteur(coord2[0]-coord1[0],coord2[1]-coord1[1])  