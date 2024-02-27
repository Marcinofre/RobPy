class Moteur :
	"""
		Modélisation d'un moteur du robot de Sorbonne Université
	"""
	def __init__(self, name:str, state:int = 1 ) -> None:
		"""
			Constructeur d'un moteur
			arg name 	: Nom du moteur
			arg state 	: etat du moteur 	--> inactive (par défaut)
											--> activeForward (vers l'avant du robot)
											--> activeBackward
			
		"""
		
		self._name = name
		self.state = state
		self.vitesseMoteur = 0  # Scalaire de la vitesse du Moteur, par défaut 0
		self.incrementVitesseMoteur = 0.1 




