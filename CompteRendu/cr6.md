# Compte Rendu de la séance

- 7eme entrevue avec le client  :

	- Objectif :
		
		- A ajouter :
			- Creation de fonction de plus haut niveau pour le controleur :
				- get_distance() 			: renvoie la distance entre le robot et l'obstacle le plus proche
				- get_time_passed()			: renvoie le temps passer entre le premier appel et le temps courant
				- get_distance_parcourue() 	: renvoie la distance parcourue
				- get_angle() 				: ???
			
			- Creer Adaptateur :
				- Creation d'une classe fille :
					- --> RobotSimuler
					- Implementation de l'api :
						- Creation robotAdpateur (c'est le frere de robotSimuler qui parler une autre langue)
					- Creation robotFake (c'est un etranger)
	
		- Refacto :
			- Rendre generique le RobotSimule 
			- Rename variable in english 
			- On retire le dossier "Module"
			- Fichier *.py en minuscule --> 2 sec
			- Nom de module en majuscule --> 2 sec
			- Moteur sa degage :
				- Les moteur du robot devienne un scalaire ---> vitesse
			- Capteur.py disparait --> dans le fichier robot.py contient class capteur
			- On retire le generateur --> utilisation du temps courant (module time)
			- Obstacle.py on le retire --> dans le fichier environnement.py contient class obstacle.py
			- Reorganistaion Controleur :
				- Un super classe controleur generique qui prends en parametre une liste de strat
				- Retirer le while (boucle) des controleurs
				- AvancerDroit : Changement de while --> if, vitesse = distance - parcourue (pour choper le reste)
				- TournerDirect : Trouver une ideer (piste : calculer angle)
			- Refacto main:
				- Revoir la facon d'apperler les threads du controleur
				- Ajouter des fonction de print() de classe pour pouvoir les affciher dans le terminale 
			- Refacto Environnement :
				- Update a revoir : Initialisation appel updateEnvironnement


		Penser deja a la 3d ... :p