import tkinter
from Robot import Robot
from Obstacle import Obstacle

class Interface:
    """
        L'interface permet une représentation graphique des mouvements du robots dans l'environnements
    """
    def __init__(self,width,height, agent : Robot):
        """
            Constructeur de la classe Interface :
            arg width  -> largeur de l'interface graphique
            arg height -> hauteur de l'interface graphique
            arg agent  -> Le robot qui se déplace dans l'interface graphique

            ---

            Attributs d'instance :
            fenetre    -> Fenetre de l'interface graphique
            canvas     -> Partie de la fenetre ou l'agent sera representé
        """
        fenetre = tkinter.Tk()
        canvas = tkinter.Canvas(fenetre, width, height, bg = 'white')
        canvas.pack()
        canvas.create_rectangle(0, 0, agent.width, agent.length)

    def ajoutObstacle(self, obs):
        """
            Ajoute un obstacle dans l'interface graphique
        """
        self.canvas.create_rectangle(obs.x0, obs.y0, obs.x1, obs.y1, fill = 'black')

    def affiche(self):
        """
            Affiche la fenetre de l'interface graphique
        """
        self.fenetre.mainloop()