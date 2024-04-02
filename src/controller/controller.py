from src.controller.strategies.unitstrats import unitStrat

class SequentialController():
	
	def __init__(self, strats: list[unitStrat]) -> None:
		"""
		"""
		self.strats = strats
		self.cur = -1

	def start(self) -> None:
		"""Remet cur à -1 pour remettre le controleur sur la première instruction possible
		"""
		self.cur = -1
		for strategy in self.strats :
			strategy.start()

	def step(self) -> None:
		"""Parcours des instructions de la liste self.strats
		"""
		
		
		if self.cur<0 or self.strats[self.cur].stop():
			print("Passage à la stratégie suivante")
			if self.stop():
				print("Fin de l'ensemble des stratégies")
				return
			self.cur += 1
		else:
			self.strats[self.cur].step()
		
	def stop(self) -> bool:
		"""Condition d'arrêt de step
		"""
		return self.cur == len(self.strats)-1 and self.strats[self.cur].stop()