# Projet Python : RobPy et ses simulations...

## Description du projet RobPy

"Datayana Bot Corp." présente le projet RobPy.

Ce projet vise à satisfaire les attentes du client, qui souhaite tester de nouvelle application sur son robot. Cependant, le client ne souhaite surtout ni abîmer, ni oser risquer un quelconque dommage sur son tout nouveau et precieux prototype. C'est pourquoi il nous confie la tâche de définir un environnement de simulation virtuel afin de tester les capacités de la réplique virtuels du robot dans un univers contrôlé.

Les attentes du client sont :
- Le robot doit pouvoir faire un carré (simulation : ✅, IRL :🤏)
- Le robot doit pouvoir s'approcher d'un mur ~~le plus vite possible~~ sans le toucher (simulation : ✅, IRL :✅)
- Le robot doit pouvoir suivre une balise (simulation : 🔜, IRL :❌)

*legende :* 
 - *✅ : Test effectué, conforme aux attentes, fonctionnel*
 - *🤏 : Test effectué presque conforme mais fonctionne*
 - *🔜 : En cours d'élaboration*
 - *❌ : Non entamé*



En fonction de l'avancement des tests et de leurs validités, carte blanche nous est donné quant à l'élaboration d'autre caractéristiques du soft.

## Structure du projet

Voici l'arborescence du repo :

- 📁`./`
	- 📁`compte_rendu/` 				-> Contient l'ensemble des compte-rendus à l'issue d'une séance
	- 📁`log/`							-> Contient les fichiers `.log` au nom des fichiers qu'il représente
	- 📁`ressource/`					-> Contient les ressources/preuves de la physique
	- 📁`src/`							-> Dossier source qui abrite l'ensemble des modules nécéssaires au déroulement de la simulation ou du robot irl. Construit sur le modèle MVC (Model, View, Controller)
		
		- 📁`controller/`
			- 📁`strategies/`
				- 📄`__init__.py`			
				- 📄`metastrats.py`		-> Contient des fonctions qui compose une liste de stratégie complexe
				- 📄`unitstrats.py`		-> Contient des stratégie unitaires (stratégie qui n'est pas composer de stratégie)
			
			- 📄`seqstrat.py` 			-> Contient un lanceur de stratégie
		
		- 📁`model/`					-> Dossier contenant l'ensemble des modules nécéssaire à la simulation (et au robot irl)
			- 📄`__init__.py`
			- 📄`environment.py`		-> Contient les class `Environment`, `Obstacle`, 
			- 📄`robot.py`				-> Contient les class `Robot`, `RobotFake` et `RobotAdapter`
		
		- 📁`view/`						-> Dossier contenant l'ensemble des modules et assets nécéssaire à la visualisation 2d et 3d de la simulation
			- 📁`assets/`				-> Dossier contenant l'ensemble des assets 3D
				- `Balise.gbl`			-> Représente la balise (cf. photo)
				- `Environnement.gbl`	-> Représente l'environnmement dans lequel évolue le robot et/ou spnt présent les obstacles/balises
				- `Obstacle.gbl`		-> Représente un Obstacle
				- `Robot.gbl`			-> Représente le robot de la simulation
			
			- 📄`__init__.py`
			- 📄`interface2d.py`		-> Vision en 2d de la simulation
			- 📄`interface3d.py`		-> Vision en 3d de la Simulation
		
		- 📄`simulation_irl.py`			-> Ensemble de fonction pour setup la simualation du robot irl
		- 📄`simulation.py`				-> Ensemble de fonction pour setup la simualation du robot simulé ou mockup

	- `main.py`							-> Fichier de lancement de la simulation

## Contributeur au projet

- YAN Nanlin 🙋‍♂️
- SI MOHAMMED Yaniss 🙋‍♂️
- GU David 🙋‍♂️
- MANOUBI Taysir 🙋‍♂️ 

