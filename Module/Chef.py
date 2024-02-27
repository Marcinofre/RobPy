import time
from Module.Env.Environnement import Environnement
from Module.Contr.ControleurCarré import ControleurCarré

class chef:
	def __init__(self, env:Environnement, controller, time = 1):
		
		self.time = time
		self.env = env
		self.ctrl = controller
		self.isRunning = True


	def updateAll(self):
		"""
			Update l'ensemble des classe de la simulation
		"""
		self.env.initSimulation()
		while self.isRunning :
			self.updateController()		#---> Update le controler (et le robot par conséquence)
			self.env.update()			#---> Update l'environnement
			time.sleep(1./self.time)	#---> frame par sec 

	def updateController(self):
		"""
			Update du controleur
		"""
		if self.ctrl.stop() :
			self.ctrl.start()

			#Initialise toute les strats à 0
			for i in self.ctrl.strats :
				i.start()
		else:
			#Exécution d'un la stratégie courante
			self.ctrl.step()
			self.ctrl.strats[self.ctrl.cur].step()


