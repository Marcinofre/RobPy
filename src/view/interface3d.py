from direct.showbase.ShowBase import ShowBase


class Interface3D(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

app = Interface3D()
app.run()