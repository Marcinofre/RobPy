import tkinter
from typing import Any
from Module.Agent.Robot import Robot
from Module.Env.Obstacle import Obstacle
from Module.Env.Environnement import Environnement

class Interface:
    """
        L'interface permet une représentation graphique des mouvements du robots dans l'environnements
    """
    def __init__(self, agent : Robot, env: Environnement, width = 1280,height = 720):
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

        #Création de la fenetre
        self.fenetre = tkinter.Tk()

        #Frame acceuillant la partie visuel de l'animation, se trouve à gauche
        self.framel = tkinter.Frame(self.fenetre, 
                                    highlightbackground="black",
                                    highlightthickness=2)
        self.framel.pack(side=tkinter.LEFT)
        
        #Frame acceuillant la partie controle de la simualation, se trouve à droite
        self.framer = tkinter.Frame(self.fenetre, 
                                    height = 720, 
                                    width = 256, 
                                    highlightbackground="black",
                                    highlightthickness=2)
        self.framer.pack(side=tkinter.RIGHT)
        
        
        #Ajout du canevas à gauche avec un fond gris, avec la largeur et longeur de l'env
        self.canvas = tkinter.Canvas(self.framel, 
                                     height = env.maxReachablePoint[1], 
                                     width = env.maxReachablePoint[0], 
                                     bg = 'grey')
        self.canvas.pack()

        #Ajout de l'attribut agent et de l'environnment
        self.agent=agent

        self.displaySpeedTop = tkinter.Frame(self.framer)
        self.TextframeRight = tkinter.Frame(self.framer)
        self.TextframeLeft = tkinter.Frame(self.framer)


        self.displaySpeedTop.pack(side=tkinter.TOP, 
                                  fill = tkinter.BOTH)
        self.TextframeRight.pack(side=tkinter.RIGHT,
                                   fill=tkinter.BOTH)
        self.TextframeLeft.pack(side=tkinter.LEFT, 
                                  fill=tkinter.BOTH)

        self.vitesse_label=tkinter.Label(self.displaySpeedTop,
                                         text=f"VitesseG : {self.agent.MoteurG.vitesseMoteur}, VitesseD : {self.agent.MoteurD.vitesseMoteur}")
        self.vitesse_label.pack()


        x0 = agent.vectRightTopCorner.x + agent.posCenter[0]
        y0 = agent.vectRightTopCorner.y + agent.posCenter[1]
        
        x1 = agent.vectLeftTopCorner.x + agent.posCenter[0]
        y1 = agent.vectLeftTopCorner.y+ agent.posCenter[1]

        x2 = agent.vectLeftBottomCorner.x + agent.posCenter[0]
        y2 = agent.vectLeftBottomCorner.y + agent.posCenter[1]

        x3 = agent.vectRightBottomCorner.x + agent.posCenter[0]
        y3 = agent.vectRightBottomCorner.y + agent.posCenter[1]


        self.rob = self.canvas.create_polygon(x0, y0,
                                              x1, y1,
                                              x2, y2,
                                              x3, y3,
                                              fill="white",
                                              outline="black")
        
        self.line = self.canvas.create_line(agent.posCenter[0], 
                                            agent.posCenter[1],
                                            agent.posCenter[0]+agent.vectD.x, 
                                            agent.posCenter[1]+agent.vectD.y,
                                            arrow=tkinter.LAST,
                                            width=5, 
                                            fill="red")
        
        
        #rappelle de la fenetre, pour rafraichissement
        self.fenetre.after(50, self.update)

    def ajoutObstacle(self, obs : Obstacle):
        """
            Ajoute un obstacle dans l'interface graphique, lève une exception si il y a déjà un objet à cet endroit là
        """
        if self.canvas.find_overlapping(obs.x0, obs.y0, obs.x1, obs.y1):
            raise Exception("Il y a déjà un objet à cet endroit là")
        self.canvas.create_rectangle(obs.x0, obs.y0, obs.x1, obs.y1, fill = 'black')
 
    def update(self):
        """
            Update la fenetre de l'interface graphique
        """

        self.fenetre.after(50, self.mjAffichageVitesse)
        self.fenetre.after(50, self.mjAffichage_Robot)
        self.canvas.after(50, self.mouv)
        self.fenetre.after(50, self.update)
        self.fenetre.update()
        self.fenetre.update_idletasks()
    
    def affiche(self):
        """
            Affiche la fenêtre de l'interface graphique
        """
        self.fenetre.mainloop()

    def mouv(self):
        """
            Update la position du robot dans l'interface graphique
        """

        x0 = self.agent.vectRightTopCorner.x + self.agent.posCenter[0]
        y0 = self.agent.vectRightTopCorner.y + self.agent.posCenter[1]
        
        x1 = self.agent.vectLeftTopCorner.x + self.agent.posCenter[0]
        y1 = self.agent.vectLeftTopCorner.y + self.agent.posCenter[1]

        x2 = self.agent.vectLeftBottomCorner.x + self.agent.posCenter[0]
        y2 = self.agent.vectLeftBottomCorner.y + self.agent.posCenter[1]

        x3 = self.agent.vectRightBottomCorner.x + self.agent.posCenter[0]
        y3 = self.agent.vectRightBottomCorner.y + self.agent.posCenter[1]
        
        self.canvas.coords(self.rob, 
                           x0, y0, 
                           x1, y1, 
                           x2, y2, 
                           x3, y3)
        self.canvas.coords(self.line, 
                           self.agent.posCenter[0], 
                           self.agent.posCenter[1],
                           self.agent.posCenter[0] + self.agent.vectD.x,
                           self.agent.posCenter[1] + self.agent.vectD.y)

    def mjAffichageVitesse(self):
        vitesseG=self.agent.MoteurG.vitesseMoteur
        vitesseD=self.agent.MoteurD.vitesseMoteur
        self.vitesse_label.config(text=f"VitesseG : {vitesseG} , VitesseD : {vitesseD}")

    def mjAffichage_Robot(self):
        self.agent.avancerRobot()
