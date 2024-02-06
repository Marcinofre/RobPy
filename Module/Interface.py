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
        self.env = env

        self.displaySpeedTop = tkinter.Frame(self.framer)
        self.buttonframeRight = tkinter.Frame(self.framer)
        self.buttonframeLeft = tkinter.Frame(self.framer)


        self.displaySpeedTop.pack(side=tkinter.TOP, 
                                  fill = tkinter.BOTH)
        self.buttonframeRight.pack(side=tkinter.RIGHT,
                                   fill=tkinter.BOTH)
        self.buttonframeLeft.pack(side=tkinter.LEFT, 
                                  fill=tkinter.BOTH)

        self.vitesse_label=tkinter.Label(self.displaySpeedTop,
                                         text=f"VitesseG : {self.agent.MoteurG.vitesseMoteur}, VitesseD : {self.agent.MoteurD.vitesseMoteur}")
        self.vitesse_label.pack()

        #Mise en place des bouttons d'activation moteur
        self.stopL = tkinter.Button(self.buttonframeLeft, 
                                    text ="activateL", 
                                    command=self.activateLeft)
        self.stopR = tkinter.Button(self.buttonframeRight, 
                                    text ="activateR", 
                                    command=self.activateRight)
        
        #Dispostion en bas dans leur frame correspondante
        self.stopL.pack(side=tkinter.BOTTOM)
        self.stopR.pack(side=tkinter.BOTTOM)


        #Commande du moteur droit du robot
        self.decrR = tkinter.Button(self.buttonframeRight, 
                                    text ="-", 
                                    command=self.decreaseRightSpeed,
                                    state="disabled")
        self.incrR = tkinter.Button(self.buttonframeRight, 
                                    text ="+", 
                                    command=self.increaseRightSpeed,
                                    state="disabled")
        
        #Dispostion à droite dans leur frame correspondante
        self.decrR.pack(side=tkinter.RIGHT)
        self.incrR.pack(side=tkinter.RIGHT)

        #Commande du Moteur gauche du Robot
        self.incrL = tkinter.Button(self.buttonframeLeft, 
                                    text ="+", 
                                    command=self.increaseLeftSpeed,
                                    state="disabled")
        self.decrL = tkinter.Button(self.buttonframeLeft, 
                                    text ="-", 
                                    command=self.decreaseLeftSpeed,
                                    state="disabled")
        
        #Disposition à gauche dans leur frame correspondante
        self.incrL.pack(side=tkinter.LEFT)
        self.decrL.pack(side=tkinter.LEFT)


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
        
        
        
        self.fenetre.bind('<Key>',self.showKeyEvent)
        self.fenetre.bind('a', self.decreaseRightSpeed)
        self.fenetre.bind('z', self.increaseRightSpeed)
        self.fenetre.bind('e', self.activateRight)
        self.fenetre.bind('i', self.decreaseLeftSpeed)
        self.fenetre.bind('o', self.increaseLeftSpeed)
        self.fenetre.bind('p', self.activateLeft)
        
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

    def showKeyEvent(self,event):
        print('Vous avez appuyé sur : ', repr(event.char))

    def decreaseRightSpeed(self, event=None):
        """
            Réduit la vitesse du robot lors d'un event
        """
        
        #Réduction de la vitesse du moteur concerné
        self.agent.MoteurD.reduitVitesse()

        #calcule de la nouvelle moyenne du robot
        self.agent.calcVitesseMoyenne()
        print(f"réduction vitesse : {self.agent.vitesseMoyenne}")
    
    def increaseRightSpeed(self, event=None):
        """
            Augmente la vitesse du robot lors d'un event
        """
        
        #Augmentation de la vitesse du moteur concerné
        self.agent.MoteurD.augmenteVitesse()

        #calcule de la nouvelle moyenne du robot
        self.agent.calcVitesseMoyenne()
        print(f"augmente vitesse : {self.agent.vitesseMoyenne}")


    def activateRight(self, event=None) :
        if self.agent.MoteurD.state == "inactive":
            
            #Active le moteur droit
            self.agent.MoteurD.activeMoteur()

            #Active les boutons de vitesse du moteur droit
            self.incrR.config(state="normal")
            self.decrR.config(state="normal")

            #Affichage console
            print("Moteur droit activé")
        else :
            
            #Desactive le moteur droit
            self.agent.MoteurD.desactiveMoteur()

            #Désactive les boutons de vitesse pour le moteur droit
            self.incrR.config(state="disabled")
            self.decrR.config(state="disabled")
            
            #Affichage console
            print("Moteur droit desactivé")
    
    def activateLeft(self, event=None) :
        if self.agent.MoteurG.state == "inactive":
            #Active le moteur gauche
            self.agent.MoteurG.activeMoteur()
            
            #Active les boutons de vitesse pour le moteur gauche
            self.incrL.config(state="normal")
            self.decrL.config(state="normal")
            print("Moteur gauche activé")
        else :
            #Desactive le moteur gauche
            self.agent.MoteurG.desactiveMoteur()
            
            #Desactive les boutons de vitesse pour le moteur gauche
            self.incrL.config(state="disabled")
            self.decrL.config(state="disabled")
            
            #Affichage console
            print("Moteur gauche desactivé")


    def decreaseLeftSpeed(self, event=None):
        """
            Réduit la vitesse du robot lors d'un event
        """
        
        #Réduction de la vitesse du moteur concerné
        self.agent.MoteurG.reduitVitesse()

        #calcule de la nouvelle moyenne du robot
        self.agent.calcVitesseMoyenne()
        print(f"réduction vitesse : {self.agent.vitesseMoyenne}")
    
    def increaseLeftSpeed(self, event=None):
        """
            Augmente la vitesse du robot lors d'un event
        """
        
        #Augmentaion de la vitesse du moteur concerné
        self.agent.MoteurG.augmenteVitesse()

        #calcule de la nouvelle moyenne du robot
        self.agent.calcVitesseMoyenne()
        print(f"augmente vitesse : {self.agent.vitesseMoyenne}")
    

    
