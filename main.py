"""Lanceur de la simulation
"""
# -IMPORT ZONE--------------------------------------------------------------------------
from src.simulation import simulation

# -CONSTANTE---------------------------------------------------------------------------
SIZE_WORLD = (1024, 720)
FPS = 60

# -APPLICATION PRINCIPALE--------------------------------------------------------------
def main():
	simulation(SIZE_WORLD, FPS)
	
if __name__ == '__main__':
	main()