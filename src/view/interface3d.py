from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor


class Interface3D(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.scene = self.loader.loadModel("assets/Environnement.glb")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)
        self.robot = self.loader.loadModel("assets/Robot.glb")
        self.robot.setScale(10, 10, 10)
        self.robot.setPos(-4,40,4)
        self.robot.reparentTo(self.render)

app = Interface3D()
app.run()