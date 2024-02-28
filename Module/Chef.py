import time
from Module.Env.Environnement import Environnement
from Module.Contr.ControleurCarré import ControleurCarré

class chef:
	def __init__(self, env:Environnement, controler, time = 10000):
		
		self.time = time 		# ---> Temps de fps
		self.env = env			# ---> Environnement de simulation
		self.ctrl = controler	# ---> Controleur
		self.cycle = 0			# ---> Cycle courrant
		self.isRunning = True


	def updateAll(self):
		"""
			Update l'ensemble des classe de la simulation
		"""
		#Initialise la simulation
		self.env.initSimulation()
		while self.isRunning :
			self.updateController()		#---> Update le controler (et le robot par conséquence)
			self.env.update()			#---> Update l'environnement
			time.sleep(1./self.time)	#---> frame par sec 

	def updateController(self):
		"""
			Update du controleur
		"""
		#Si le cycle vient de débuter 
		if self.ctrl.stop()  :
			self.ctrl.start()

			#Initialise toute les strats à 0
			for i in self.ctrl.strats :
				i.start()
			self.cycle += 1
		else:
			#Exécution de la stratégie courante
			self.ctrl.step()
			self.ctrl.strats[self.ctrl.cur].step()


