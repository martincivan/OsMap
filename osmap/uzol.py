class Uzol:

    def __init__(self, nazov):
        self.nazov = nazov
        self.typy = set()
        self.zoznamzaznamov = {}

    def pridajzaznam(self, zaznam):
        self.typy.add(zaznam.typ)
        self.zoznamzaznamov[zaznam.typ] = zaznam

    def __str__(self):
        return self.nazov

    @property
    def zaznamy(self):
        return self.zoznamzaznamov.items()