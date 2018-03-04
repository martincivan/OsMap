from zaznam import zaznam


class kontinent:

    def __init__(self, nazov):
        self.nazov = nazov
        self.zaznamy = []

    def pridajzaznam(self, z):
        self.zaznamy.append(zaznam(z, self.nazov))
