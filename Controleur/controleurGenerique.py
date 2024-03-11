class ControleurGenerique():
    
    def __init__(self, strats):
        """
            Constructeur de la classe ControleurCarré:
            arg strats : Toutes les stratégies utilisés par le controleur
            
            ---

            Attributs d'instances :
            strats = Liste comprenant toutes les stratégies suivi par le controleur
            cur = Index permettant de désigner l'instruction qui est en train d'éxécuter (Initialisé à -1 et va jusqu'à len de strats -1)
        """
        self.strats = strats
        self.cur = -1
        self.speed = 1

    def start(self):
        """
            Remet cur à -1 pour remettre le controleur sur la première instruction possible
        """
        self.cur = -1
        for i in self.strats :
            i.speed = self.speed
            i.start()

    def step(self):
        """
            Fonction qui parcours les instructions 
        """
        print("STEP!")
        if self.stop():
            return
        if self.cur<0 or self.strats[self.cur].stop():
            self.cur+=1
    
    def stop(self):
        """
            Condition d'arrêt de step
        """
        return self.cur == len(self.strats)-1 and self.strats[self.cur].stop()