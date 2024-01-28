from Vecteur import Vecteur
from Moteur import Moteur
import os
import math

class Robot :
	"""
		Modélisation d'un robot de Sorbonne Université
	"""

	def __init__(self, width, length, x:float=0, y:float=0) -> None:
		
		self._dim = (width, length)
		
		self.vectD = Vecteur(0, 0)  # Vecteur direction, par défaut (0, 0)
        
		self.scalVitesse = 1.0  # Scalaire de la vitesse, par défaut 1.0
	
		#Position en x et y du centre du robot
		self.posCenter = (x,y)
		
		#Position globale du robot (devant, derriere, droit et gauche)
		self.posFront = (x, y + length/2)
		self.posRear = (x, y - length/2)
		self.posLeftSide = (x - (width/2), y)
		self.posRightSide = (x + (width/2), y)

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

	def parsingInstruction(self, instruction):
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
				number = int(arg[1:])
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
		self.scalVitesse = dicoparam['vitesse']
		if commande == 'avancer':
			for time in range(dicoparam['duree']):
				self.avancerRobot()
		if commande == 'reculer':
			for time in range(dicoparam['duree']):
				self.reculerRobot()
		if commande == 'tourner':
			for time in range(dicoparam['duree']):
				self.tournerRobot(dicoparam['angle'])
			

	
	def runRobot(self) :
		"""
			Mets en action le robot
		"""
		

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


 
 





	
	
