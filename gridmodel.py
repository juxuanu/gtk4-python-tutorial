from gi.repository import GObject


class File(GObject.Object):
    name = GObject.Property(type=str)

    def __init__(self, name: str):
        super().__init__()
        self.name = name
