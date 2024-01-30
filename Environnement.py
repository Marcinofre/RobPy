from Obstacle import Obstacle
from Robot import Robot
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
			setObstacle	        -> Un ensemble contenant tous les obstacles de l'environnement
		"""
		
		self.onGoing = False
		self.currentClock = 0
		self.clockPace = clockPace
		self.maxReachablePoint = (x,y)
		self.agent = agent
		setObstacle = set()



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

	
	def activateAgent(self, agent : Robot):
		agent.isActive = True
	
	def runAgent(self, agent :Robot, fileInstruction) :
		"""
			Mets en action le robot
		"""
		if agent.isActive:
			try :
				genFileInstruction = agent.readInstruction(fileInstruction)
			except:
				return
			
			var = True
			while var:
				try :
					line = next(genFileInstruction)
					#print(line)
				except:
					var = False
				
				try :
					
					comm_arg = agent.parsingInstruction(line)
					#print(comm_arg[1])
				except:
					
					continue
				
				try :
					duree = comm_arg[1]["duree"]
				except:
					duree = 1
				for i in range(int(duree)):
					next(self.clockCount())
					agent.executeInstruction(comm_arg)
					print(agent.posCenter)

		else:
			print("Agent non activé. Veuillez activer l'agent")



	def addObstacle(self, obs) :
		"""
			Prend en argument obs soit une List soit un objet de la classe Obstacle :
				- Si c'est un objet de la classe Obstacle, il est ajouté au setObstacle.
				- Si c'est une List, il parcourt la liste et chaque élément de la classe Obstacle est ajouté au setObstacle.
				- Si c'est ni l'un ni l'autre, on affiche : L'élément n'est pas un obstacle.
		"""
		if isinstance(obs, list):
			for obj in obs :
				if isinstance(obj, obs) :
					self.setObstacle.add(obj)
		elif isinstance(obs, Obstacle):
				self.setObstacle.add(obs)
		else :
			print("L'élément n'est pas un obstacle")

	def doesCollide(self, agent : Robot):
		"""
			Prend en argument un obstacle et un robot.
        	Détermine si rob est en collision avec obs, renvoie True ou False. 
			Fait un produit de produit vectoriel de la forme (AB ^ AC)(AB ^ AD) ET (CD ^ CA)(CD ^CB)
        """
		pass