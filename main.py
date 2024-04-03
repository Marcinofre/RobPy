"""Lanceur de la simulation
"""
# -IMPORT ZONE--------------------------------------------------------------------------
from src.simulation import *

# -CONSTANTE---------------------------------------------------------------------------
SIZE_WORLD = (1024, 720)
FPS = 10000

# -APPLICATION PRINCIPALE--------------------------------------------------------------
def main():
	simulation(SIZE_WORLD, FPS)

if __name__ == '__main__':
	main()