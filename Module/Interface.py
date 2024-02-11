import itertools
import tkinter
from Module.Env.Obstacle import Obstacle


class Interface:
    """
        L'interface permet une représentation graphique des mouvements du robots dans l'environnements
    """
    def __init__(self, env, width = 1280,height = 720):
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

        #Ajout de l'environnment comme attribut
        self.env=env

        #Création de zone prédeterminé (une l'affichage de la vitesse)
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
                                         text=f"VitesseG : {self.env.agent.MoteurG.vitesseMoteur}, VitesseD : {self.env.agent.MoteurD.vitesseMoteur}")
        self.zone_saisie_vitesse = tkinter.Entry(self.TextframeRight)
        self.vitesse_label.pack()
        self.zone_saisie_vitesse.pack()

        initialPosition = env.agent.getCarcasse()
        self.rob = self.canvas.create_polygon(*initialPosition,
                                              fill="white",
                                              outline="black")
        
        self.line = self.canvas.create_line(*self.env.agent.posCenter,
                                            self.env.agent.posCenter[0]+self.env.agent.vectD.x, 
                                            self.env.agent.posCenter[1]+self.env.agent.vectD.y,
                                            arrow=tkinter.LAST,
                                            width=5, 
                                            fill="red")
        
        
        #rappelle de la fenetre, pour rafraichissement
        self.fenetre.after(50, self.update)

    #Voir source de cette fonction : https://stackoverflow.com/questions/32449670/tkinter-tclerror-bad-screen-distance-in-pythons-tkinter-when-trying-to-modi
    def flatten(self, list_of_lists):
        """Flatten one level of nesting"""
        return itertools.chain.from_iterable(list_of_lists)

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
        position = self.env.agent.getCarcasse()
        self.canvas.coords(self.rob, 
                           *self.flatten(position))
        self.canvas.coords(self.line, 
                           self.env.agent.posCenter[0], 
                           self.env.agent.posCenter[1],
                           self.env.agent.posCenter[0] + self.env.agent.vectD.x,
                           self.env.agent.posCenter[1] + self.env.agent.vectD.y)

    def mjAffichageVitesse(self):
        vitesseG=self.env.agent.MoteurG.vitesseMoteur
        vitesseD=self.env.agent.MoteurD.vitesseMoteur
        self.vitesse_label.config(text=f"VitesseG : {vitesseG}, VitesseD : {vitesseD}")