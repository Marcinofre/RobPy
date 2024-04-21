from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import Mat4
from panda3d.core import LineSegs


class Interface3D(ShowBase):

    def __init__(self, env):
        ShowBase.__init__(self)
        self.env = env
        self.scene = self.loader.loadModel("src/view/assets/Environnement.glb")
        self.scene.reparentTo(self.render)
        self.scene.setScale(self.env._area_max[0], 1, self.env._area_max[1])
        self.scene.setPos(0, 0, -10)
        self.scene.setHpr(0,-90,0)
        self.robot = self.loader.loadModel("src/view/assets/Robot.glb")
        self.robot.setScale(self.env._robot._dim[0], 30, self.env._robot._dim[1])
        self.robot.setPos(self.env._robot._position_x,self.env._robot._position_y,23)
        self.robot.setHpr(self.env._robot._total_theta,-90,0)
        self.robot.reparentTo(self.render)
        self.taskMgr.add(self.moveRobot, "MoveRobotTask")
        self.accept("space", self.resetCam)
        self.line = LineSegs("lines")
        self.line.setColor(1,1,1,1)
        self.line.moveTo(self.robot.getPos().getX(), self.robot.getPos().getY(), self.robot.getPos().getZ())

    def moveRobot(self, task):
        position = self.env._robot.get_position()
        self.robot.setPos(position[0], position[1],23)
        self.robot.setHpr(self.env._robot._total_theta,-90,0)
        self.line.drawTo(position[0], position[1],23)
        self.linenode = self.line.create(False)
        self.render.attachNewNode(self.linenode)
        return Task.cont
    
    def resetCam(self):
        self.disableMouse()
        position = self.robot.getPos()
        self.camera.setPos(position.getX(), position.getY()-300, position.getZ()+70)
        self.camera.lookAt(self.robot)
        mat = Mat4(self.camera.getMat())
        mat.invertInPlace()
        self.mouseInterfaceNode.setMat(mat)
        self.enableMouse()