# Compte Rendu de la séance

- 5eme entrevue avec le client  :
	- Point Positif :
		- "Vous êtes pas trop nul, mais vous faites des trucs aussi nul que les autres" *said the client*
	
	
	- Point Négatif	:
		- Code trop brouillon
			- Manque de lisibitlité, on doit pouvoir comprendre le code en un simple coup d'oeil (au moins savoir de quoi on parle)
		- Retirer les boucles dans le controleur
		- Plus de rigueur dans le code
		- ATTENTION à bien montrer la même version que la version main 

	
	- Ce qu'il faut faire :
		- Refactoriser : rendre plus compréhensible le code
			- Réécrire les variables en quelques chose de plus lisible
		- Le trello doit être faisable, ni trop court, ni trop long
		- Revoir la méchanique de mouvement du robot 
		- refaire le main :
			-	Retirer les boucle présent dans le controleur
			-	Ajouter un main qui update l'environnement et le controlleur
		- Pour la démo :
			- Le robot doit pouvoir foncer dans un mur le plus vite possible sans s'y cogner
			- Ce qui signifie  :
				- Avoir un Capteur de distance :
					- Capable de :
						- Dire si un objet est devant lui ou non (boolean + dist obj ?) :
							- Projection d'un rayon à x distance (x valeur arbitraire ?)
								- Creation d'un vecteur unitaire ? (x = norme du vecteur unitaire ?)

							- Est-ce que le rayon coupe quelque chose dans l'environnement ? (appel l'environnement ?)
							- Valeur de retour ?
						- De balayer une zone :
							- tourner : 
								- à droite 
								- à gauche
				- Une stratégie du type FoncerSansCrasher composé de stratégie 'élémentaire' ou une seul stratégie ?
