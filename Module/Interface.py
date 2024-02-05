import tkinter
from typing import Any
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
        self.framel = tkinter.Frame(self.fenetre, 
                                    height = 720, 
                                    width = 1024,
                                    highlightbackground="black",
                                    highlightthickness=2)
        self.framel.pack(side=tkinter.LEFT)
        self.framer = tkinter.Frame(self.fenetre, 
                                    height = 720, 
                                    width = 256, 
                                    highlightbackground="black",
                                    highlightthickness=2)
        self.framer.pack(side=tkinter.RIGHT)
        self.canvas = tkinter.Canvas(self.framel, 
                                     width=1024, 
                                     height=720, 
                                     bg = 'grey')
        self.canvas.pack()

        self.agent=agent

        self.buttonframe = tkinter.Frame(self.framer)
        self.buttonframe.pack(fill=tkinter.BOTH)

        self.vitesse_label=tkinter.Label(self.buttonframe,text="VitesseG : 0 , VitesseD : 0")
        self.vitesse_label.pack()

        self.stopL = tkinter.Button(self.buttonframe, text ="activateL", command=self.activateLeft)
        self.stopL.pack(side=tkinter.BOTTOM)

        self.stopR = tkinter.Button(self.buttonframe, text ="activateR", command=self.activateRight)
        self.stopR.pack(side=tkinter.BOTTOM)

        self.decrR = tkinter.Button(self.buttonframe, text ="-", command=self.decreaseRightSpeed)
        self.decrR.pack(side=tkinter.RIGHT)

        self.incrR = tkinter.Button(self.buttonframe, text ="+", command=self.increaseRightSpeed)
        self.incrR.pack(side=tkinter.RIGHT)

        self.incrL = tkinter.Button(self.buttonframe, text ="+", command=self.increaseLeftSpeed)
        self.incrL.pack(side=tkinter.LEFT)
        
        self.decrL = tkinter.Button(self.buttonframe, text ="-", command=self.decreaseLeftSpeed)
        self.decrL.pack(side=tkinter.LEFT)


        self.mjAffichageVitesse()
        self.mjAffichage_Robot()

        rect_width = agent._dim[0]
        rect_height = agent._dim[1]
        x0 = ((1024 - rect_width) / 2) + agent.posCenter[0]
        y0 = ((720 - rect_height) / 2) + agent.posCenter[1]
        x1 = x0 + rect_width + agent.posCenter[0]
        y1 = y0 + rect_height + agent.posCenter[1]
        self.rob = self.canvas.create_rectangle(x0, y0, x1, y1)
        self.line = self.canvas.create_line((x0+x1)/2, 
                                (y0+y1)/2,
                                (x0+x1)/2+agent.vectD.x, 
                                (y0+y1)/2+agent.vectD.y,
                                arrow=tkinter.LAST)
        self.canvas.after(50, self.mouv, agent)
        self.fenetre.after(50, self.update)
        
        self.fenetre.bind('<Key>',self.showKeyEvent)
        self.fenetre.bind('a', self.decreaseRightSpeed)
        self.fenetre.bind('z', self.increaseRightSpeed)
        self.fenetre.bind('e', self.activateRight)
        self.fenetre.bind('i', self.decreaseLeftSpeed)
        self.fenetre.bind('o', self.increaseLeftSpeed)
        self.fenetre.bind('p', self.activateLeft)

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
        self.fenetre.update()
        self.fenetre.update_idletasks()
        self.fenetre.after(50, self.update)
    
    def affiche(self):
        """
            Affiche la fenêtre de l'interface graphique
        """
        self.fenetre.mainloop()

    def mouv(self, agent : Robot):
        """
            Update la position du robot dans l'interface graphique
        """
        rect_width = agent._dim[0]
        rect_height = agent._dim[1]
        x0 = ((1024 - rect_width) / 2) + agent.posCenter[0]
        y0 = ((720 - rect_height) / 2) + agent.posCenter[1]
        x1 = x0 + rect_width + agent.posCenter[0]
        y1 = y0 + rect_height + agent.posCenter[1]
        self.canvas.coords(self.rob, x0, y0, x1, y1)
        xcen = (x0+x1)/2
        ycen = (y0+y1)/2
        self.canvas.coords(self.line, xcen, ycen, xcen+ agent.vectD.x, ycen + agent.vectD.y)
        self.canvas.after(50, self.mouv, agent)



    def mjAffichageVitesse(self):
        vitesseG=self.agent.MoteurG.vitesseMoteur
        vitesseD=self.agent.MoteurD.vitesseMoteur
        self.vitesse_label.config(text=f"VitesseG : {vitesseG} , VitesseD : {vitesseD}")
        self.fenetre.after(50,self.mjAffichageVitesse)

    def mjAffichage_Robot(self):
        self.agent.avancerRobot()
        self.fenetre.after(50,self.mjAffichage_Robot)

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
            self.agent.MoteurD.activeMoteur()
            print("Moteur droit activé")
        else :
            self.agent.MoteurD.desactiveMoteur()
            print("Moteur droit desactivé")
    
    def activateLeft(self, event=None) :
        if self.agent.MoteurG.state == "inactive":
            self.agent.MoteurG.activeMoteur()
            print("Moteur gauche activé")
        else :
            self.agent.MoteurG.desactiveMoteur()
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
    

    
