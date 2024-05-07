"""Lanceur de la simulation
"""
# -IMPORT ZONE--------------------------------------------------------------------------
from src.simulation_irl import simulation

# -CONSTANTE---------------------------------------------------------------------------
SIZE_WORLD = (1024, 720)
FPS = 600

# -APPLICATION PRINCIPALE--------------------------------------------------------------
def main():
	simulation(SIZE_WORLD, FPS)
	
if __name__ == '__main__':
	main()