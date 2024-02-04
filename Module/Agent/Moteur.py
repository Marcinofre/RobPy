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
		self.Vitesse = 1.0  # Scalaire de la vitesse du Moteur, par défaut 1.0


	def accelere(self,acceleration) :
		"""
			Augmente la vitesse du Moteur
		"""
		self.Vitesse = self.Vitesse * acceleration

	def ralentie(self,ralentissement) :
		"""
			Ralentie la vitesse du Moteur
		"""
		self.Vitesse = self.Vitesse / ralentissement



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


	#pour l'instant YNL 
	def vitesse_set(self,nouv_vitesse):
		"""
			modifier la vitesse
		"""
		self.Vitesse=nouv_vitesse
		
		
