# -IMPORT ZONE---------------------------------------------------------------------------
from src.controller.strategies.unitstrats import UnitStrat
import logging
# ---------------------------------------------------------------------------------------

# -Logging setup-------------------------------------------------------------------------

logger = logging.getLogger(__name__)
formatter = logging.Formatter('INFO : %(message)s')

# Niveau de logging
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
# ---------------------------------------------------------------------------------------

# -CONTROLLER----------------------------------------------------------------------------
class SequentialStrategy(UnitStrat):
	
	def __init__(self, strats: list[UnitStrat]) -> None:
		"""
		"""
		self.strats = strats

	def start(self) -> None:
		"""Remet cur à -1 pour remettre le controleur sur la première instruction possible
		"""
		self.cur = -1

	def step(self) -> None:
		"""Parcours des instructions de la liste self.strats
		"""
		if self.cur<0 or self.strats[self.cur].stop_strat:
			logger.info("Passage à la stratégie suivante")
			if self.stop():
				logger.info("Fin de l'ensemble des stratégies")
				return
			self.cur += 1
		else:
			self.strats[self.cur].step()
		
	def stop(self) -> bool:
		"""Condition d'arrêt de step
		"""
		return self.cur == len(self.strats)-1 and self.strats[self.cur].stop_strat
