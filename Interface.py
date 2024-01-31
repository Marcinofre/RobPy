import tkinter
from Robot import Robot

class Interface:
    """
        L'interface permet une représentation graphique des mouvements du robots dans l'environnements
    """
    def __init__(self,width,height, agent : Robot):
        fenetre = tkinter.Tk()
        canvas = tkinter.Canvas(fenetre, width, height, bg = 'white')
        canvas.pack()
        canvas.create_rectangle(0, 0, agent.width, agent.length)
        fenetre.mainloop()