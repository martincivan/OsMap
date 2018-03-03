from kontinent import kontinent


class typ:
    typy = {}
    zoznamTypov = ["Europe", "Asia"]

    def __init__(self, t):
        self.typ = t
        for zTyp in self.zoznamTypov:
            self.typy[zTyp] = kontinent(zTyp)

    def pridajZaznam(self, z):
        self.typy[z.tag].pridajZaznam(z)
