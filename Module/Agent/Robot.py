from Vecteur import Vecteur
import os
import math
from Moteur import Moteur

class Robot :
	"""
		Modélisation d'un robot de Sorbonne Université
	"""

	def __init__(self, width, length, x:float=0, y:float=0) -> None:
		"""
			Constructeur de la classe Robot :
			arg width : Largeur du robot
			arg length : Longueur du robot

			---

			Attribut d'instance env. :
			dim				-> Dimension du robot défini par sa largeur et sa longueur
			isActive		-> Booléen qui définit si le robot est allumé ou non
			scalVitesse		-> Scalaire définissant la vitesse du robot
			vectD 	        -> Vecteur direction du mouvement du robot
			posCenter       -> Position du centre du robot dans l'environnement défini par x et y (initialisé à 0,0)
		"""
		
		self._dim = (width, length)

		self.MoteurD = Moteur

		self.MoteurG = Moteur

		self.rayon = 0.25
		" rayon du cercle passant par les deux roues en mètres, à définir, 0.25 n'est qu'une valeur abstraite" 

		self.isActive = False
		
		self.vectD = Vecteur(0, 0)  # Vecteur direction, par défaut (0, 0)
        
		self.scalVitesse = 5.0  # Scalaire de la vitesse, par défaut 1.0
	
		#Position en x et y du centre du robot
		self.posCenter = (x,y)

	def VitesseAngulaire(self) :
		"""
			Permet de faire tourner le vecteur direction quand une roue va plus vite que l'autre.
		"""
		if self.MoteurD.Vitesse != self.MoteurG.Vitesse :
		# Fonctionne seulement si les vitesses des deux moteurs ne sont pas égales.
			
			# Cas 1 : Le moteur droit est le plus rapide, on tourne à gauche
			if self.MoteurD.Vitesse > self.MoteurG.Vitesse :
				diff = self.MoteurD.Vitesse - self.MoteurG.Vitesse
				angle = diff / self.rayon
				pi = math.pi
				angle = angle * ( 180/pi )
				self.vectD.rotationAngle(-angle)

			# Cas 2 : Le moteur gauche est le plus rapide, on tourne à droite
			if self.MoteurG.Vitesse > self.MoteurD.Vitesse :
				diff = self.MoteurG.Vitesse - self.MoteurD.Vitesse
				angle = diff / self.rayon
				pi = math.pi
				angle = angle * ( 180/pi )
				self.vectD.rotationAngle(angle)


	def allPos(self) :
		"""
			Print l'ensemble des positions disponible du robot
		"""
		print(f"Position du robot : {self.posCenter}")

	def readInstruction(self, instructionFile):
		"""
			Lis les instructions d'un fichier script
			arg instrcutionFile --> fichier .txt contenant une suite d'instruction pour le robot
		"""
		if not os.path.exists(instructionFile):
			raise Exception("File not found. Or file doesn't exist")
		else :
			with open(instructionFile,"r") as file:
				for line in file:
					yield line

	def parsingInstruction(self, instruction : str):
		"""
			Récupère l'instruction d'un fichier (une ligne) et parse les éléments de cette commande pour récupérer les paramètres et l'instruction			arg instrcution --> chaine de caractère contenant la commande à parser
			format de texte : <instruction>: <param1> <param2> etc...
			retourne un tuple (<instruction>, list[parametre])
		"""
		instruction = instruction.lower()
		sep = ":"
		index = instruction.find(sep)
		command = instruction[0:index]
		parameter = instruction[index+1:].split(" ")
		dicoArg = dict()
		for arg in parameter:
			try:
				number = float(arg[1:])
			except:
				raise ValueError(f"{arg[1:]} is not a number")
			
			if arg[0] == 'd':
				if number <= 0:
					number = 1
				dicoArg['duree'] = number
			if arg[0] == 'r':
				dicoArg['angle'] = number
			if arg[0] == 'v':
				dicoArg['vitesse'] = number

		return (command, dicoArg)
	
	def executeInstruction(self, dicInstruction):
		"""
			Exécute une commande en fonction de l'instruction du premier élement du tuple et de la liste de parametre
			arg instruction --> tuple (<instruction>, dico[param])
		"""

		commande, dicoparam = dicInstruction
		try :
			self.scalVitesse = dicoparam['vitesse']
		except:
			pass
	
		if commande == 'avancer':
			self.avancerRobot()
		if commande == 'reculer':
			self.reculerRobot()
		if commande == 'tourner':
			try :
				self.tournerRobot(dicoparam['angle'])
			except :
				raise Exception("No value 'Angle'")
		

	def avancerRobot(self):
		"""
			Met à jour la position du robot en le faisant avancer en fonction de la vitesse et du vecteur direction
		"""
		self.posCenter = (round(self.posCenter[0] + (self.vectD.x * self.scalVitesse), 1), round(self.posCenter[1]+ (self.vectD.y * self.scalVitesse ), 1))
    
	def reculerRobot(self):
		"""
			Met à jour la position du robot en le faisant reculer en fonction de la vitesse et du vecteur direction
		"""
		self.posCenter = (round(self.posCenter[0] + (self.vectD.x * (- self.scalVitesse)), 1), round(self.posCenter[1]+ (self.vectD.y * (- self.scalVitesse) ), 1))
    
	def tournerRobot(self,deg):
		"""
			Modifie la direction du vecteur direction en fonction de la valeur en degrés de paramètre deg 
		"""
		self.vectD.rotationAngle(deg)


 
 





	
	
