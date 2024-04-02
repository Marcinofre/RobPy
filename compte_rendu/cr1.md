# Compte Rendu de la séance

- Deuxème entrevue avec le client, les points à retenir ~~du remonter de bretelle~~ de la réunion :
	
	- **Attention** a la gestion du trello :
		- Une tache : 
			- Fonction de 3-4 lignes (en gros, pas très long)
			- Pas durée plus d'une trentaine de minute
			- Exception de durée pour les tâches du type documentation/formation
			- On a rarement 1h/2h sans interruption devant soit donc tâche courte
		
		- ce qui est dans **Done**  doit être au préablable *vérifier*.
		-  La vérification se fait **PAR UN AUTRE** et surtout **PAS PAR LUI MÊME**
			- Par des exercices (*en lien avec le projet*)
			- Question/Réponse
		- Toutes les tâches de la semaine doivent être dans **Done** lors de la prochaine entrevue avec le client.
			- Si une tache semble durer sur plusieurs semaine :
				- Tâche beaucoup trop ouverte. 
					- Doit être mieux parsé en des tâches + faisable dans le crénaux de la semaine
		- Mieux équilibrer les tâches
		- Plus de discussion au sein de l'equipe
		- Pas de découverte au fur et à mesure du code
		- Revoir l'utilisation de branche Github :
			- Une branche **N'EST PAS** une branche personnelle
			- Si **pas de conflit** avec ce qui est déjà dévellopé, alors branche **PAS** *nécéssaire*
			- Une branche  :
				- doit correspondre au travail sur **_UNE feature_** 
				- Doit être *vérifié* par tierce
				- Doit être *merge* à la branche *principale*/*dev*
				- Doit être *supprimé* ensuite
		
		- Rappel de l'objectif de l'UE :
			- C'est travail de groupe, pas un travail individuel
			- Le **but** *n'est pas* que le projet marche, mais que **le processus de réalisation** *soit en adéquation* avec la méthode **SCRUM/Agile**
			- L'évaluation se fait sur le travail d'équipe ~~oui, ça se répète mais au cas oú l'info passe mieux XD~~

## Princpale objectif de la semaine

- Temps de consacré au projet :
	- Yaniss : 2~3 heures 
	- David  : 4 heures
	- Nanlin : 4 heures
	- Taysir : 4 heures ~~c'est moins que la derniere fois hein...~~

- Présentation promise au client :
	- **"Le robot suit un script prédéterminé inscrit dans un fichier texte"**

- Pour ce faire :
	- À creer :
		- Définir un classe Vecteur pour permettre les opérations nécéssaire sur les vecteurs :
			- Fonctions nécéssaires (pour le moment) :
				- Constructeur de Vecteur
				- Rotation d'un vecteur selon un angle 
				- Calcul du produit scalaire de deux vecteurs
				- Multiplication scalaire d'un vecteur
				- Calcul de la norme

		- Définir des fonctions dans la classe Robot :
			- lecture de script
			- de parsing de script + vérification
			- puis d'éxécution de ce script
		- Définir des fonctions dans la classe Robot :
			- Actions associés aux instructions du script :
				- Avancer
				- reculer
				- Tourner
			- une action = une instruction
		- Modifier la fonction runRobot en conséquence
		- Revoir le code de Simulation.py ?
		- Comment gèrer la vitesse et le temps de l'environnement ?



		- Optionnel (si plus de temps) :
			- Création d'une classe Obstacle
			- Ajout de fonction dans l'environnement :
				- Fonction de positionnement de l'obstacle si c'est possible
		
		- Mise au point des avancées Vendredi après-midi
