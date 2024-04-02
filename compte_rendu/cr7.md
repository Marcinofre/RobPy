# Compte Rendu de la séance

- 8eme entrevue avec le client  :

	- Objectif :
		
		- A ajouter :
			- Creation de fonction de plus haut niveau pour le controleur :
				- get_time_passed()			: renvoie le temps passer entre le premier appel et le temps courant
				- get_distance_parcourue() 	: renvoie la distance parcourue en deltat temps
				- get_angle() 				: Angle parcourue en deltat temps
			
		- Ré-implémentation de l'adapteur:
            - MOTOR_RIGHT et MOTOR_LEFT : constante des ports
            - set_motor_dps : Utilisation avec les nouveaux ports
            - Suppression des différentes coordonné et attributs utilisés dans le fakeRobot
            - Suppression héritage de RobotSimuler dans robotAdapteur
            - Ajout d'un if permettant d'empecher le lancement de l'interface avec le robotAdapteur
	
		- Refacto :
			- On rajoute un dossier 'simpack'
			- On retourne en séquentielle -> Suppression du threqding
			- Reorganistaion Controleur :
				Utilisation des fonctions de plus haut niveau
			- Refacto main:
				- Suppression du threading
                - Ajout fonction runSimulation pour effectuer la simulation en séquentielle
			- Refacto Environnement :
				- Passage variable agent à robot
            - Refacto Robot :
                - Passage vitesseAngulaire en minuscule
            - Refacto Interface:
                - Capacité à pouvoir tourner en séquentielle le robot avec l'interface (mainloop de tkinter pose problème)


