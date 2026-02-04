from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3
from direct.task import Task

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Disable kamera default
        self.disableMouse()

        # Load environment
        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25)
        self.scene.setPos(-8, 42, 0)

        # Player (kotak)
        self.player = self.loader.loadModel("models/box")
        self.player.reparentTo(self.render)
        self.player.setScale(1)
        self.player.setPos(0, 0, 1)

        # Kamera
        self.camera.setPos(0, -10, 5)
        self.camera.lookAt(self.player)

        # Kontrol
        self.keys = {"w": False, "s": False, "a": False, "d": False}
        self.accept("w", self.set_key, ["w", True])
        self.accept("w-up", self.set_key, ["w", False])
        self.accept("s", self.set_key, ["s", True])
        self.accept("s-up", self.set_key, ["s", False])
        self.accept("a", self.set_key, ["a", True])
        self.accept("a-up", self.set_key, ["a", False])
        self.accept("d", self.set_key, ["d", True])
        self.accept("d-up", self.set_key, ["d", False])

        self.taskMgr.add(self.update, "update")

    def set_key(self, key, value):
        self.keys[key] = value

    def update(self, task):
        dt = globalClock.getDt()
        speed = 5

        if self.keys["w"]:
            self.player.setY(self.player, speed * dt)
        if self.keys["s"]:
            self.player.setY(self.player, -speed * dt)
        if self.keys["a"]:
            self.player.setX(self.player, -speed * dt)
        if self.keys["d"]:
            self.player.setX(self.player, speed * dt)

        # Kamera follow
        self.camera.setPos(
            self.player.getX(),
            self.player.getY() - 10,
            self.player.getZ() + 5
        )
        self.camera.lookAt(self.player)

        return Task.cont

game = Game()
game.run()
