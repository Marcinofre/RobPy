from Environnement import Environnement as env
from Robot import Robot as rob

rpy = rob(0,0,0,0)
en = env(15,15, rpy)

pressedKey = input("Press k to start the simulation, another key to quit --> ")

if pressedKey == 'k' :
	passNumber = False
	while not passNumber :
		maxIt = input("Choose the number of maximum iteration --> ")
		try :
			maxIt = int(maxIt)
			passNumber = True
		except ValueError :
			print("Usage : Only number allowed")
			passNumber = False
			


	#Initialisation de l'environnment
	print("Initialisation de l'environnment")
	en.runEnv()

	#Initialisation du générateur
	print("Initialisation du générateur")
	genTime = en.clockCount()
	

	print("After each step, you can press q to quit or any other key to continue the next iteration of the simulation")

	while True :
		
		wantoquit = input("q to quit, else to continue : ")
		if wantoquit == 'q':
			break
		elif en.currentClock >= maxIt :
			print(f"Max iteration reached : {en.currentClock}")
			break
		else:
			print(f"Generation {next(genTime)}")
			en.agent.runRobot()
			if en.isOut() :
				break
			en.agent.allPos()



print("Fin de la simulation")
