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
        self.scene.setScale(self.env._area_max[0]/2, 1, self.env._area_max[1]/2)
        self.scene.setPos(self.env._area_max[0]/2, self.env._area_max[1]/2, -10)
        self.scene.setHpr(0, -90, 0)
        
        # Ajout du modele de l'environnement dans le render, rotation et changement du positionnement pour aider l'affichage
        self.robot = self.loader.loadModel("src/view/assets/Robot.glb")
        self.robot.setScale(self.env._robot._dim[0]/2, 30, self.env._robot._dim[1]/2)
        self.robot.setPos(self.env._robot._position_x + self.env._robot._dim[0]/2, self.env._robot._position_y + self.env._robot._dim[1], 23)
        self.robot.setHpr(self.env._robot._total_theta, -90, 0)
        self.robot.reparentTo(self.render)
        
        # Ajout dans le task manager de moveRobot
        self.taskMgr.add(self.moveRobot, "MoveRobotTask")
       
        # Lorsque l'on appuie sur espace, l'interface utilisera la fonction resetCam
        self.accept("a", self.resetCam)
        self.accept("z", self.abovePOV)
        self.accept("e", self.robotPOV)

        # Creation de la ligne tracant les mouvements du robots
        self.line = LineSegs("lines")
        self.line.setColor(1, 1, 1, 1)
        self.line.moveTo(self.robot.getPos().getX(), self.robot.getPos().getY(), self.robot.getPos().getZ())
        self.addObs()
        
        # Camera mode variables
        self.firstPersonMode = False

    def moveRobot(self, task):
        """Rafraichit la position du robot dans l'affichage et trace le passage du robot
        """
        # On récupère la position actuelle du robot
        position = self.env._robot.get_position()
       
        # On change directement la position du robot dans l'affichage
        self.robot.setPos(position[0] + self.env._robot._dim[0]/2, position[1] + self.env._robot._dim[1]/2, 23)
        
        # On change la rotation du robot dans l'affichage
        self.robot.setHpr(-math.degrees(self.env._robot._total_theta), -90, 0)
        
        # On trace et ajoute la ligne representant le deplacement entre les 2 points
        self.line.drawTo(position[0] + self.env._robot._dim[0]/2, position[1] + self.env._robot._dim[1]/2, 23)
        self.linenode = self.line.create(False)
        self.render.attachNewNode(self.linenode)
        
        # Si la camera est en mode premiere personne on doit l'update de la meme facon qu'on a implementer robotPOV
        if self.firstPersonMode:
            robot_pos = self.robot.getPos()
            robot_hpr = self.robot.getHpr()

            offset_distance = (self.env._robot._dim[0]/2)+1
            offset_x = offset_distance * math.cos(math.radians(robot_hpr[0]))
            offset_y = offset_distance * math.sin(math.radians(robot_hpr[0]))
            self.camera.setPos(self.robot.getPos())
            self.camera.setHpr(self.robot.getHpr())
            camera_pos = (robot_pos[0] + offset_x, robot_pos[1] + offset_y, robot_pos[2] + 1.0)
        
            self.camera.setPos(camera_pos)
            self.camera.setHpr(robot_hpr[0]-90 + math.degrees(self.env._robot._captor_theta)-90, 0, 0)
        
        # Permet à la tache de se faire en boucle
        return Task.cont

    def addObs(self):
        obs = []
        taille = []
        position = []
        x = 0
        y = 0
        for obst in self.env.get_obstacles():
            taille.append((obst.origin[0], 23, obst.origin[1]))
            for obsx in range(obst.origin[0], obst.end[0] + 1):
                x = obsx
                y = obst.origin[1]
                position.append((x, y, 23))
                obs.append(self.loader.loadModel("src/view/assets/Obstacle.glb"))
            for obsx in range(obst.origin[0], obst.end[0] + 1):
                x = obsx
                y = obst.end[1]
                position.append((x, y, 23))
                obs.append(self.loader.loadModel("src/view/assets/Obstacle.glb"))
            for obsy in range(obst.origin[1], obst.end[1] + 1):
                x = obst.origin[0]
                y = obsy
                position.append((x, y, 23))
                obs.append(self.loader.loadModel("src/view/assets/Obstacle.glb"))
            obs.append(self.loader.loadModel("src/view/assets/Obstacle.glb"))
            for obsy in range(obst.origin[1], obst.end[1] + 1):
                x = obst.end[0]
                y = obsy
                position.append((x, y, 23))
                obs.append(self.loader.loadModel("src/view/assets/Obstacle.glb"))

            position.append((x, y, 23))
        for model, pos in zip(obs, position):
            model.reparentTo(self.render)
            model.setPos(pos)
            model.setScale(1, 23, 1)
            model.setHpr(0, -90, 0)

    def resetCam(self):
        """Repositionne la camera de sorte a regarder le robot
        """
        # Désactive la fonction de la souris de bouger la camera
        self.disableMouse()
        
        # On récupère la position du robot
        position = self.robot.getPos()
       
        # Bouge la camera par rapport à la position du robot
        self.camera.setPos(position.getX(), position.getY() + 300, position.getZ() + 70)
        
        # lookAt permet de changer la rotation de la camera de telle sorte à ce qu'elle regarde le robot
        self.camera.lookAt(self.robot)
        
        # On crée une Matrice4 à partir de la position de la caméra et on modifie mouseInterfaceNode avec cette matrice inversée
        mat = Mat4(self.camera.getMat())
        mat.invertInPlace()
        self.mouseInterfaceNode.setMat(mat)
        
        # Ré-active la souris
        self.enableMouse()
        self.firstPersonMode = False

    def abovePOV(self):
        """Repositionne la camera au-dessus du robot"""
        # Désactive la fonction de la souris de bouger la camera
        self.disableMouse()
        
        # On récupère la position du robot
        position = self.robot.getPos()
       
        # Bouge la camera par rapport à la position du robot
        self.camera.setPos(position.getX(), position.getY(), position.getZ() + 300)
        
        # lookAt permet de changer la rotation de la camera de telle sorte à ce qu'elle regarde le robot
        self.camera.lookAt(self.robot)
        
        # On crée une Matrice4 à partir de la position de la caméra et on modifie mouseInterfaceNode avec cette matrice inversée
        mat = Mat4(self.camera.getMat())
        mat.invertInPlace()
        self.mouseInterfaceNode.setMat(mat)
        
        # Ré-active la souris
        self.enableMouse()
        self.firstPersonMode = False

    def robotPOV(self):
        """Positionne la caméra a la face avant du Robot"""
        self.disableMouse()
        
        #On calcule l'offset et on prend la pos et le hpr du robot
        offset = (self.env._robot._dim[0]/2)+1
        robot_pos = self.robot.getPos()
        robot_hpr = self.robot.getHpr()
        
        # On calcule l'offset en x et y avec cos et sin et on modifie la pos de la camera
        offset_x = offset * math.cos(math.radians(robot_hpr[0]))
        offset_y = offset * math.sin(math.radians(robot_hpr[0]))
        
        pos = (robot_pos[0] + offset_x, robot_pos[1] + offset_y, robot_pos[2] + 1)
        
        self.camera.setPos(pos)
        # !! On fait -90 car la camera commence a regarder a gauche et pas directement en face du robot
        self.camera.setHpr(robot_hpr[0]-90 + math.degrees(self.env._robot._captor_theta) -90, 0, 0)

        self.firstPersonMode = True