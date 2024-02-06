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
		self.vitesseMoteur = 0  # Scalaire de la vitesse du Moteur, par défaut 0
		self.incrementVitesseMoteur = 0.1 


	def augmenteVitesse(self) :
		"""
			augmente la vitesse de 1 
		"""
		self.vitesseMoteur = round(self.vitesseMoteur+self.incrementVitesseMoteur, 1)

	def reduitVitesse(self) :
		"""
			reduit la vitesse de 1 
		"""
		self.vitesseMoteur = round(self.vitesseMoteur-self.incrementVitesseMoteur,1)
	
	def activeMoteur(self):
		""" 
			Change l'etat du moteur en 'active'
		"""
		self.state = "active"

	def desactiveMoteur(self) :
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
		
		
