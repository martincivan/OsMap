from zaznam import Zaznam


class Kontinent:

    def __init__(self, nazov):
        self.nazov = nazov
        self.zaznamy = []

    def pridajzaznam(self, z):
        self.zaznamy.append(Zaznam(z, self.nazov))
