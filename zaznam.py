

class Zaznam:

    def __init__(self, z, kon):
        self.typ = z.tag
        self.atrib = z.attrib
        self.kont = kon

    @property
    def nazov(self):
        return self.atrib['name']

    def pekny_nazov(self):
        bodka = self.nazov.find('.')
        if bodka > 0:
            vysledok = self.nazov[int(0) : int(bodka)]
            vysledok = vysledok.lower()
            vysledok = vysledok.replace(self.typ, '')
            vysledok = vysledok.replace('_', ' ')
            return vysledok.strip().title()