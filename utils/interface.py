"""
    Module correspondant à la partie graphique de la simulation (GUI), son lancement est optionnel.
"""
import itertools
from Controleur.controleurCarre import ControleurCarre
from Controleur.controleurCollision import ControleurCollision
import tkinter
from Env.environnement import Obstacle

class Interface():
    """
        L'interface permet une représentation graphique de la simulation
    """
    def __init__(self, environment, controller, width = 1280,height = 720):
        """
            Initialise la window graphique et ses éléments qui la compose

            Args:
                width: Largeur de l'interface graphique
                height: Hauteur de l'interface graphique
                controller: Controleur de l'agent

            Attributes:
                window: Fenetre de l'interface graphique
                frame_left: Frame contenant le canvas et prenant 80% de la largeur de la fenêtre
                frame_right: Frame contenant les différents widget permettant de manipuler les attributs et prenant 20% de la fenêtre
                canvas: Partie de la window, dans frame_left, ou l'agent sera representé
        """


        #Ajout de l'environnment et du controller comme attribut
        self.environment = environment
        self.controller = controller

        #Création de la window
        self.window = tkinter.Tk()

        #Frame acceuillant la partie visuel de l'animation, se trouve à gauche
        self.frame_left = tkinter.Frame(self.window, 
                                    highlightbackground="black",
                                    highlightthickness=2)
        self.frame_left.pack(side=tkinter.LEFT)
        
        #Frame acceuillant la partie controle de la simualation, se trouve à droite
        self.frame_right = tkinter.Frame(self.window, 
                                    height = 720, 
                                    width = 256, 
                                    highlightbackground="black",
                                    highlightthickness=2)
        self.frame_right.pack(side=tkinter.RIGHT)
        
        
        #Ajout du canevas à gauche avec un fond gris, avec la largeur et longeur de l'environment
        self.canvas = tkinter.Canvas(self.frame_left, 
                                     height = environment.maxReachablePoint[1], 
                                     width = environment.maxReachablePoint[0], 
                                     bg = 'grey')
        self.canvas.pack()

        

        #Création de zone prédeterminé (une l'affichage de la vitesse)
        self.display_top = tkinter.Frame(self.frame_right)
        self.textframe_right = tkinter.Frame(self.frame_right)
        self.textframe_left = tkinter.Frame(self.frame_right)
        self.textframe_bottom = tkinter.Frame(self.frame_right)

        #Positionnement des différentes frame
        self.textframe_bottom.pack(side=tkinter.BOTTOM, 
                                 fill=tkinter.BOTH)
        self.display_top.pack(side=tkinter.TOP,
                                  fill = tkinter.BOTH)
        self.textframe_right.pack(side=tkinter.RIGHT,
                                 fill=tkinter.BOTH)
        self.textframe_left.pack(side=tkinter.LEFT, 
                                 fill=tkinter.BOTH)

        self.speed_label = tkinter.Label(self.display_top,
                                         text=f"VitesseG : {environment.agent.MoteurG}, VitesseD : {environment.agent.MoteurD}")
        self.time_label = tkinter.Label(self.display_top,
                                         text=f"Temps Courant : {environment.currentClock}")
        

        #definition des variables d'acceuil des entrees
        self.speedmotor_right = tkinter.DoubleVar()
        self.speedmotor_left = tkinter.DoubleVar()

        self.paceTime = tkinter.DoubleVar()
        self.paceTime.set(1)

        #Définition des label et de leurs zone d'entrée respective
        self.label_vitesseMD = tkinter.Label(self.textframe_left, text="Vitesse Moteur droit :" )
        self.label_vitesseMG = tkinter.Label(self.textframe_left, text="Vitesse Moteur gauche :" )
        self.label_pacetime = tkinter.Label(self.textframe_left, text="Pas de temps :" )
        self.zone_saisie_vitesseMD = tkinter.Entry(self.textframe_right, textvariable=self.speedmotor_right)
        self.zone_saisie_vitesseMG = tkinter.Entry(self.textframe_right, textvariable=self.speedmotor_left)
        self.zone_saisie_pacetime = tkinter.Entry(self.textframe_right, textvariable=self.paceTime)

        #Position des labels d'affichage
        self.time_label.pack(side=tkinter.TOP)
        self.speed_label.pack()
        
        #Position des zone de saisie et leur label
        self.label_vitesseMD.pack()
        self.zone_saisie_vitesseMD.pack()

        self.label_vitesseMG.pack()
        self.zone_saisie_vitesseMG.pack()
        
        self.label_pacetime.pack()
        self.zone_saisie_pacetime.pack()

        #Définition d'un bouton d'envoie
        buttonEnvoie = tkinter.Button(self.textframe_bottom,
                                 text="Envoie",
                                 command=self.dispatch_order)
        
        buttonStop = tkinter.Button(self.textframe_bottom,
                                 text="Stop",
                                 command=self.stop)
        
        buttonRun = tkinter.Button(self.textframe_bottom,
                                 text="Lancer",
                                 command=self.run)
        
        #Positionnement des boutons
        buttonEnvoie.pack()
        buttonStop.pack()
        buttonRun.pack()


        
        #Dessin Robot initial
        initialPosition = environment.agent.getCarcasse()                   #--> Récupère la carcasse du robot (pour dessiner ses contours)
        self.rob = self.canvas.create_polygon(*initialPosition,
                                              fill="white",
                                              outline="black")
        
        #Dessin d'une fleche représentant le vecteur direction
        self.line = self.canvas.create_line(*self.environment.agent.posCenter,
                                            self.environment.agent.posCenter[0]+self.environment.agent.vectD.x, 
                                            self.environment.agent.posCenter[1]+self.environment.agent.vectD.y,
                                            arrow=tkinter.LAST,
                                            width=5, 
                                            fill="red")
        self.line2 = self.canvas.create_line(*self.environment.agent.posCenter,
                                            self.environment.agent.posCenter[0]+self.environment.agent.capteur.ray.x, 
                                            self.environment.agent.posCenter[1]+self.environment.agent.capteur.ray.y,
                                            arrow=tkinter.LAST,
                                            width=5, 
                                            fill="pink")
        
        
        #rappelle de la window, pour rafraichissement
        self.window.after(50, self.update_all)

    #Voir source de cette fonction : https://stackoverflow.com/questions/32449670/tkinter-tclerror-bad-screen-distance-in-pythons-tkinter-when-trying-to-modi
    def flatten(self, list_of_lists):
        """Flatten one level of nesting"""
        return itertools.chain.from_iterable(list_of_lists)

    def add_obstacle(self, obs : Obstacle):
        """
            Ajoute un obstacle dans l'interface graphique, lève une exception si il y a déjà un objet à cet endroit là
        """
        if self.canvas.find_overlapping(obs.x0, obs.y0, obs.x1, obs.y1):
            raise Exception("Il y a déjà un objet à cet endroit là")
        self.canvas.create_rectangle(obs.x0, obs.y0, obs.x1, obs.y1, fill = 'black')
    
    def display_interface(self):
        """
            Affiche la fenêtre de l'interface graphique
        """
        self.window.mainloop()

    def update_canvas(self):
        """
            Mets a jour la position du robot dans l'interface graphique
        """
        position = self.environment.agent.getCarcasse()
        position_ray = self.environment.agent.getForInterfaceRay()
        self.canvas.coords(self.rob, 
                           *self.flatten(position))
        self.canvas.coords(self.line, 
                           *self.environment.agent.posCenter,
                           self.environment.agent.posCenter[0] + self.environment.agent.vectD.x*self.environment.agent._dim[0]/2,
                           self.environment.agent.posCenter[1] + self.environment.agent.vectD.y*self.environment.agent._dim[1]/2)
        self.canvas.coords(self.line2, 
                           *self.environment.agent.posCenter,
                            self.environment.agent.posCenter[0] + position_ray.x,
                            self.environment.agent.posCenter[1] + position_ray.y)

    def update_labels(self):
        """
            Mise a jour des affichages des labels de l'interfaces
        """

        #Mise a jour de l'affichage de la vitesse des moteurs
        left_speed = self.environment.agent.MoteurG
        right_speed = self.environment.agent.MoteurD
        self.speed_label.config(text=f"VitesseG : {left_speed}, VitesseD : {right_speed}")

        #Mise à jour de l'affichage du temps courant
        self.time_label.config(text=f"Temps Courant : {self.environment.currentClock}")

    def dispatch_order(self):
        self.environment.agent.MoteurD = round(self.speedmotor_right.get(), 1)
        self.environment.agent.MoteurG = round(self.speedmotor_left.get(), 1)
        self.environment.clockPace = round(self.paceTime.get(),1)
    
    def update_all(self):
        
        self.update_canvas()

        #Mise a jour de l'affichage des labels 
        self.update_labels()
        
        
        #Trace le passage du robot sur le Canevas
        self.draw_path()

        self.window.update()
        self.window.update_idletasks()
        self.window.after(50, self.update_all)

    
    def run(self):
        if isinstance(self.controller, ControleurCarre) or isinstance(self.controller, ControleurCollision):
            speed = (self.speedmotor_left.get() + self.speedmotor_right.get())/2
            if speed > 0 :
                self.controller.speed = speed
                print("LA VITESSE EST MODIFIEE")
            self.controller.start()
        self.environment.agent.isControlled = True
    
    def stop(self):
        self.environment.agent.isControlled = False


    def draw_path(self):
       """
            Trace le passage du robot
       """
       for position in self.environment.agent.trace:
          self.canvas.create_oval(
            position[0] - 2, position[1] - 2, 
            position[0] + 2, position[1] + 2, 
               fill='blue' )
