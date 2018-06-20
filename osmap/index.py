from pygtrie import CharTrie
from osmap.uzol import Uzol
from osmap.zaznam import Zaznam

class Index:

    def __init__(self):
        self.zoznamkrajin = set()
        self.uzly = {}
        self.strom = CharTrie()
        self.strom.enable_sorting(enable=True)


    def pridajzaznam(self, zaznam):
        name = zaznam.attrib['name'].split("_")
        if name[0].lower() == 'hillshade':
            name.remove(name[0])
        nazov = name[0]
        if len(name) > 3:
            nazov += '-'
            nazov += name[1]
        if nazov not in self.zoznamkrajin:
            self.zoznamkrajin.add(nazov)
            self.uzly[nazov] = Uzol(nazov)
        self.uzly[nazov].pridajzaznam(Zaznam(zaznam))

    def hladaj(self, text):
        return self.strom.itervalues(prefix=text.lower())

    def spravstrom(self):
        for i in self.uzly:
            self.strom[i.lower()] = self.uzly[i]
            print("Pridal som: "+i.lower() + ", " + str(self.uzly[i]))
