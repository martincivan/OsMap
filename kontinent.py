from zaznam import zaznam


class kontinent:
    zaznamy = []

    def __init__(self, nazov):
        self.nazov = nazov

    def pridajZaznam(self, z):
        self.zaznamy.append(zaznam(z))
