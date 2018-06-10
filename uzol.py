class Uzol:

    def __init__(self, nazov):
        self.nazov = nazov
        self.typy = set()
        self.zaznamy = {}

    def pridajzaznam(self, zaznam):
        self.typy.add(zaznam.typ)
        self.zaznamy[zaznam.typ] = zaznam

    def __str__(self):
        return self.nazov