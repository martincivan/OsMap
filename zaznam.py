

class zaznam:

    def __init__(self, z, kon):
        self.typ = z.tag
        self.atrib = z.attrib
        self.kont = kon

    @property
    def nazov(self):
        return self.atrib['name']
