import tkinter
from Module.Agent.Robot import Robot
from Module.Env.Obstacle import Obstacle

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
        self.fenetre = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.fenetre, width=width, height=height, bg = 'white')
        self.canvas.pack()
        self.canvas.create_rectangle(agent._dim[0]/2, agent._dim[1]/2, -agent._dim[0]/2, -agent._dim[1]/2)

    def ajoutObstacle(self, obs):
        """
            Ajoute un obstacle dans l'interface graphique
        """
        if self.canvas.find_overlapping(obs.x0, obs.y0, obs.x1, obs.y1):
            raise Exception("Il y a déjà un objet à cet endroit là")
        self.canvas.create_rectangle(obs.x0, obs.y0, obs.x1, obs.y1, fill = 'black')

    def affiche(self):
        """
            Affiche la fenetre de l'interface graphique
        """
        self.fenetre.mainloop()