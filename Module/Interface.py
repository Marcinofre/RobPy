import tkinter
from Module.Agent.Robot import Robot
from Module.Env.Obstacle import Obstacle

class Interface:
    """
        L'interface permet une représentation graphique des mouvements du robots dans l'environnements
    """
    def __init__(self, agent : Robot, width = 1280,height = 720):
        """
            Constructeur de la classe Interface :
            arg width  -> largeur de l'interface graphique
            arg height -> hauteur de l'interface graphique
            arg agent  -> Le robot qui se déplace dans l'interface graphique

            ---

            Attributs d'instance :
            fenetre    -> Fenetre de l'interface graphique
            framel     -> Frame contenant le canvas et prenant 80% de la fenêtre
            framer     -> Frame contenant les différents widget permettant de manipuler les attributs et prenant 20% de la fenêtre
            canvas     -> Partie de la fenetre, dans framel, ou l'agent sera representé
        """
        self.fenetre = tkinter.Tk()
        self.framel = tkinter.Frame(self.fenetre, height = 720, width = 1024, highlightbackground="black",highlightthickness=2)
        self.framel.pack(side=tkinter.LEFT)
        self.framer = tkinter.Frame(self.fenetre, height = 720, width = 256, highlightbackground="black",highlightthickness=2)
        self.framer.pack(side=tkinter.RIGHT)
        self.canvas = tkinter.Canvas(self.framel, width=1024, height=720, bg = 'gray')
        self.canvas.pack()
        rect_width = agent._dim[0]
        rect_height = agent._dim[1]
        x0 = (1024 - rect_width) / 2
        y0 = (720 - rect_height) / 2
        x1 = x0 + rect_width
        y1 = y0 + rect_height
        self.canvas.create_rectangle(x0, y0, x1, y1)
        self.canvas.create_line(agent.posCenter[0], agent.posCenter[1], agent.posCenter[0]+agent.vectD.x, agent.posCenter[1]+agent.vectD.y)
        self.fenetre.mainloop()

    def ajoutObstacle(self, obs : Obstacle):
        """
            Ajoute un obstacle dans l'interface graphique, lève une exception si il y a déjà un objet à cet endroit là
        """
        if self.canvas.find_overlapping(obs.x0, obs.y0, obs.x1, obs.y1):
            raise Exception("Il y a déjà un objet à cet endroit là")
        self.canvas.create_rectangle(obs.x0, obs.y0, obs.x1, obs.y1, fill = 'black')

    def update(self):
        """
            Affiche la fenetre de l'interface graphique
        """
        self.fenetre.update()
        self.fenetre.update_idletasks()