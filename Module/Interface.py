import itertools
from threading import Thread
import tkinter
from Module.Env.Obstacle import Obstacle


class Interface():
    """
        L'interface permet une représentation graphique des mouvements du robots dans l'environnements
    """
    def __init__(self, env, controleur, width = 1280,height = 720):
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


        #Ajout de l'environnment et du controleur comme attribut
        self.env = env
        self.ctrl = controleur

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

        

        #Création de zone prédeterminé (une l'affichage de la vitesse)
        self.displayTop = tkinter.Frame(self.framer)
        self.TextframeRight = tkinter.Frame(self.framer)
        self.TextframeLeft = tkinter.Frame(self.framer)
        self.TextframeBottom = tkinter.Frame(self.framer)

        #Positionnement des différentes frame
        self.TextframeBottom.pack(side=tkinter.BOTTOM, 
                                 fill=tkinter.BOTH)
        self.displayTop.pack(side=tkinter.TOP,
                                  fill = tkinter.BOTH)
        self.TextframeRight.pack(side=tkinter.RIGHT,
                                 fill=tkinter.BOTH)
        self.TextframeLeft.pack(side=tkinter.LEFT, 
                                 fill=tkinter.BOTH)

        self.vitesse_label=tkinter.Label(self.displayTop,
                                         text=f"VitesseG : {env.agent.MoteurG.vitesseMoteur}, VitesseD : {env.agent.MoteurD.vitesseMoteur}")
        self.temps_label= tkinter.Label(self.displayTop,
                                         text=f"Temps Courant : {env.currentClock}")
        

        #definition des variables d'acceuil des entrees
        self.vitesseMD = tkinter.DoubleVar()
        self.vitesseMG = tkinter.DoubleVar()

        self.paceTime  = tkinter.DoubleVar()

        #Définition des label et de leurs zone d'entrée respective
        self.label_vitesseMD = tkinter.Label(self.TextframeLeft, text="Vitesse Moteur droit :" )
        self.label_vitesseMG = tkinter.Label(self.TextframeLeft, text="Vitesse Moteur gauche :" )
        self.labe_pacetime = tkinter.Label(self.TextframeLeft, text="Pas de temps :" )
        self.zone_saisie_vitesseMD = tkinter.Entry(self.TextframeRight, textvariable=self.vitesseMD)
        self.zone_saisie_vitesseMG = tkinter.Entry(self.TextframeRight, textvariable=self.vitesseMG)
        self.zone_saisie_pacetime = tkinter.Entry(self.TextframeRight, textvariable=self.paceTime)

        #Position des labels d'affichage
        self.temps_label.pack(side=tkinter.TOP)
        self.vitesse_label.pack()
        
        #Position des zone de saisie et leur label
        #self.label_vitesseMD.pack()
        #self.zone_saisie_vitesseMD.pack()

        #self.label_vitesseMG.pack()
        #self.zone_saisie_vitesseMG.pack()
        
        #self.labe_pacetime.pack()
        #self.zone_saisie_pacetime.pack()

        #Définition d'un bouton d'envoie
        boutton = tkinter.Button(self.TextframeBottom,
                                 text="Envoie",
                                 command=self.dispatchVariableCommande)
        
        #Positionnement des boutons
        boutton.pack()
        

        
        #Dessin Robot initial
        initialPosition = env.agent.getCarcasse()                   #--> Récupère la carcasse du robot (pour dessiner ses contours)
        self.rob = self.canvas.create_polygon(*initialPosition,
                                              fill="white",
                                              outline="black")
        
        #Dessin d'une fleche représentant le vecteur direction
        self.line = self.canvas.create_line(*self.env.agent.posCenter,
                                            self.env.agent.posCenter[0]+self.env.agent.vectD.x, 
                                            self.env.agent.posCenter[1]+self.env.agent.vectD.y,
                                            arrow=tkinter.LAST,
                                            width=5, 
                                            fill="red")
        self.line2 = self.canvas.create_line(*self.env.agent.posCenter,
                                            self.env.agent.posCenter[0]+self.env.agent.capteur.ray.x, 
                                            self.env.agent.posCenter[1]+self.env.agent.capteur.ray.y,
                                            arrow=tkinter.LAST,
                                            width=5, 
                                            fill="pink")
        
        
        #rappelle de la fenetre, pour rafraichissement
        self.fenetre.after(50, self.updateAll)

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
    
    def affiche(self):
        """
            Affiche la fenêtre de l'interface graphique
        """
        self.fenetre.mainloop()

    def updateCanevas(self):
        """
            Update la position du robot dans l'interface graphique
        """
        position = self.env.agent.getCarcasse()
        position_ray = self.env.agent.getForInterfaceRay()
        self.canvas.coords(self.rob, 
                           *self.flatten(position))
        self.canvas.coords(self.line, 
                           *self.env.agent.posCenter,
                           self.env.agent.posCenter[0] + self.env.agent.vectD.x,
                           self.env.agent.posCenter[1] + self.env.agent.vectD.y)
        self.canvas.coords(self.line2, 
                           *self.env.agent.posCenter,
                            self.env.agent.posCenter[0] + position_ray.x,
                            self.env.agent.posCenter[1] + position_ray.y)

    def mjAffichageLabel(self):
        """
            Mise a jour des affichages des labels de l'interfaces
        """

        #Mise a jour de l'affichage de la vitesse des moteurs
        vitesseG=self.env.agent.MoteurG.vitesseMoteur
        vitesseD=self.env.agent.MoteurD.vitesseMoteur
        self.vitesse_label.config(text=f"VitesseG : {vitesseG}, VitesseD : {vitesseD}")

        #Mise à jour de l'affichage du temps courant
        self.temps_label.config(text=f"Temps Courant : {self.env.currentClock}")

    def dispatchVariableCommande(self):
        self.env.agent.MoteurD.vitesseMoteur = round(self.vitesseMD.get(), 1)
        self.env.agent.MoteurG.vitesseMoteur = round(self.vitesseMG.get(), 1)
        self.env.clockPace = round(self.paceTime.get(),1)
    
    def updateAll(self):
        position = self.env.agent.getCarcasse()
        position_ray = self.env.agent.getForInterfaceRay()
        self.canvas.coords(self.rob, 
                           *self.flatten(position))
        self.canvas.coords(self.line, 
                           *self.env.agent.posCenter,
                           self.env.agent.posCenter[0] + self.env.agent.vectD.x,
                           self.env.agent.posCenter[1] + self.env.agent.vectD.y)
        self.canvas.coords(self.line2, 
                           *self.env.agent.posCenter,
                            self.env.agent.posCenter[0] + position_ray.x,
                            self.env.agent.posCenter[1] + position_ray.y)
        
        #Mise a jour de l'affichage de la vitesse des moteurs
        vitesseG=self.env.agent.MoteurG.vitesseMoteur
        vitesseD=self.env.agent.MoteurD.vitesseMoteur
        self.vitesse_label.config(text=f"VitesseG : {vitesseG}, VitesseD : {vitesseD}")

        #Mise à jour de l'affichage du temps courant
        self.temps_label.config(text=f"Temps Courant : {self.env.currentClock}")

        self.fenetre.update()
        self.fenetre.update_idletasks()
        self.fenetre.after(50, self.updateAll)