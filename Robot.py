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
		
		self.vectD = Vecteur(0, 0)  # Vecteur direction par défaut (0, 0)
        
		self.vectV = Vecteur(0, 0)  # Vecteur vitesse par défaut (0, 0)
	
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
			format de texte : <instruction>: <param1> <param2> etc...\\n
		"""
		instruction = instruction.lower()
		sep = ":"
		index = instruction.find(sep)
		command = instruction[0:index]
		parameter = instruction[index+1:]
		
		return (command, parameter)


	
	
	
	def runRobot(self) :
		"""
			Fais rouler le robot dans la direction du vecteur vitesse
		"""
		self.posCenter = (self.posCenter[0] + self.vectV[0], self.posCenter[1] + self.vectV[1])

	def avancerRobot(self):
		"""
			Met à jour la position du robot en le faisant avancer vers l'avant en fonction du vecteur vitesse et direction
		"""
		self.posCenter=(self.posCenter[0]+(self.vectD*(Vecteur.calcNorm(self.vectV.x))) , self.posCenter[1]+(self.vectD*(Vecteur.calcNorm(self.vectV.y))))
    
	def reculerRobot(self):
		"""
			Met à jour la position du robot en le faisant avancer vers l'arrière en fonction du vecteur vitesse et direction
		"""
		self.posCenter=(self.posCenter[0]+(self.vectD*(-Vecteur.calcNorm(self.vectV.x))) , self.posCenter[1]+(self.vectD*(-Vecteur.calcNorm(self.vectV.y))))
    
	def tournerRobot(self,deg):
		"""
			Modifie la direction du vecteur direction en fonction de la valeur en degrés de paramètre deg 
		"""
		self.vectD.rotationAngle(deg)

 
 





	
	
