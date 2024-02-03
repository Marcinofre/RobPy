class Moteur :
	"""
		Modélisation d'un moteur du robot de Sorbonne Université
	"""
	def __init__(self, name, state = "inactive") -> None:
		"""
			Constructeur d'un moteur
			arg name 	: Nom du moteur
			arg state 	: etat du moteur 	--> inactive (par défaut)
											--> activeForward (vers l'avant du robot)
											--> activeBackward
			
		"""
		
		self._name = name
		self.state = state
		self.Vitesse = 1.0  # Scalaire de la vitesse, par défaut 1.0
		

	def add_accelere(self,acceleration) :
		"""
			Augmente la vitesse du moteur en addition
		"""
		self.Vitesse = self.Vitesse + acceleration


	def mult_accelere(self,acceleration) :
		"""
			Augmente la vitesse du moteur en multiplication
		"""
		self.Vitesse = self.Vitesse * acceleration



	def avance(self) :
		"""
			Change l'etat du moteur en 'activeForward' 
		"""
		self.state = "activeForward"
	
	def recule(self) :
		"""
			Change l'etat du moteur en 'activeBackward' 
		"""
		self.state = "activeBackward"
	
	def stop(self) :
		""" 
			Change l'etat du moteur en 'inactive'
		"""
		self.state = "inactive"
		
