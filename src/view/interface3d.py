from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import Mat4
from panda3d.core import LineSegs
import math

class Interface3D(ShowBase):

    def __init__(self, env):
        """Class Interface3D correspondant à la partie graphique de l'environnement (GUI)

		Attributes:
			Elements:
				env (Environment): Environnement de simulation à afficher

			Window:
				render : Affichage de Panda3D
				Composition:
					Model : 
                        scene : Modele de l'environnement
                        robot : Modele du robot
					line : Ligne permettant de tracer les mouvements du robot

	"""
        ShowBase.__init__(self)
        
        # Ajout du modele de l'environnement dans le render, rotation et changement du positionnement pour aider l'affichage
        self.env = env
        self.scene = self.loader.loadModel("src/view/assets/Environnement.glb")
        self.scene.reparentTo(self.render)
        self.scene.setScale(self.env._area_max[0], 1, self.env._area_max[1])
        self.scene.setPos(self.env._area_max[0]/2, self.env._area_max[1]/2, -10)
        self.scene.setHpr(0,-90,0)
        
        # Ajout du modele de l'environnement dans le render, rotation et changement du positionnement pour aider l'affichage
        self.robot = self.loader.loadModel("src/view/assets/Robot.glb")
        self.robot.setScale(self.env._robot._dim[0], 30, self.env._robot._dim[1])
        self.robot.setPos(self.env._robot._position_x+self.env._robot._dim[0]/2,self.env._robot._position_y+self.env._robot._dim[1],23)
        self.robot.setHpr(self.env._robot._total_theta,-90,0)
        self.robot.reparentTo(self.render)
        
        # Ajout dans le task manager de moveRobot
        self.taskMgr.add(self.moveRobot, "MoveRobotTask")
       
        # Lorsque l'on appuie sur espace, l'interface utilisera la fonction resetCam
        self.accept("a", self.resetCam)
        self.accept("z", self.abovePOV)
        
        # Creation de la ligne tracant les mouvements du robots
        self.line = LineSegs("lines")
        self.line.setColor(1,1,1,1)
        self.line.moveTo(self.robot.getPos().getX(), self.robot.getPos().getY(), self.robot.getPos().getZ())
        self.addObs()

    def moveRobot(self, task):
        """Rafraichit la position du robot dans l'affichage et trace le passage du robot
        """
        
        #On récupère la position actuelle du robot
        position = self.env._robot.get_position()
       
        #On change directement la position du robot dans l'affichage
        self.robot.setPos(position[0]+self.env._robot._dim[0]/2, position[1]+self.env._robot._dim[1]/2,23)
        
        #On change la rotation du robot dans l'affichage
        self.robot.setHpr(-math.degrees(self.env._robot._total_theta),-90,0)
        
        #On trace et ajoute la ligne representant le deplacement entre les 2 points
        self.line.drawTo(position[0]+self.env._robot._dim[0]/2, position[1]+self.env._robot._dim[1]/2,23)
        self.linenode = self.line.create(False)
        self.render.attachNewNode(self.linenode)
        
        #Permet à la tache de se faire en boucle
        return Task.cont
    
    def addObs(self):
        obs = []
        position = []
        taille = []
        for obst in self.env.get_obstacles() :
            x = (obst.origin[0] + obst.end[0])/2
            y = (obst.origin[1] + obst.end[1])/2
            d = math.sqrt((obst.end[0] -obst.origin[0]) **2 + (obst.end[1] - obst.origin[1])**2)
            obs.append(self.loader.loadModel("src/view/assets/Obstacle.glb"))
            position.append((x,y,23))
            taille.append((d*math.cos(math.radians(45)), 
                           30,
                           d*math.sin(math.radians(45))))
        for model,pos,t in zip(obs,position,taille):
            model.reparentTo(self.render)
            model.setPos(pos)
            model.setScale(t)
            model.setHpr(0,-90,0)

    def resetCam(self):
        """Repositionne la camera de sorte a regarder le robot
        """
       
        #On désactive la fonction de la souris de bouger la camera pour pouvoir modifier la position de la camera a travers des lignes de commande
        self.disableMouse()
        
        #On récupère la position du robot
        position = self.robot.getPos()
       
        #On bouge la camera par rapport a la position du robot, les differentes valeurs de X et Y peuvent etre modifiés
        self.camera.setPos(position.getX(), 
                           position.getY()+300, 
                           position.getZ()+70)
        
        #lookAt permet de changer la rotation de la camera de telle sorte a ce qu'elle regarde le robot
        self.camera.lookAt(self.robot)
        
        #On crée une Matrice4 à partir de la position de la caméra et on modifie mouseInterfaceNode avec cette matrice inversée
        mat = Mat4(self.camera.getMat())
        mat.invertInPlace()
        self.mouseInterfaceNode.setMat(mat)
        
        #On ré-active la souris, si on avait pas fait l'etape d'avant, la camera n'aurait pas bouger
        self.enableMouse()
    
    def abovePOV(self):
        
        #On désactive la fonction de la souris de bouger la camera pour pouvoir modifier la position de la camera a travers des lignes de commande
        self.disableMouse()
        
        #On récupère la position du robot
        position = self.robot.getPos()
       
        #On bouge la camera par rapport a la position du robot, les differentes valeurs de X et Y peuvent etre modifiés
        self.camera.setPos(position.getX(), position.getY(), position.getZ()+300)
        
        #lookAt permet de changer la rotation de la camera de telle sorte a ce qu'elle regarde le robot
        self.camera.lookAt(self.robot)
        
        #On crée une Matrice4 à partir de la position de la caméra et on modifie mouseInterfaceNode avec cette matrice inversée
        mat = Mat4(self.camera.getMat())
        mat.invertInPlace()
        self.mouseInterfaceNode.setMat(mat)
        
        #On ré-active la souris, si on avait pas fait l'etape d'avant, la camera n'aurait pas bouger
        self.enableMouse()

        