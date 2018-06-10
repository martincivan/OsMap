from pygtrie import Trie
from uzol import Uzol
from zaznam import Zaznam

class Index:

    def __init__(self):
        self.zoznamkrajin = set()
        self.uzly = {}
        self.strom = Trie()
        self.strom.enable_sorting(enable=True)


    def pridajzaznam(self, zaznam):
        name = zaznam.attrib['name'].split("_")
        nazov = name[0]
        if len(name) > 3:
            nazov += '-'
            nazov += name[1]
        if nazov not in self.zoznamkrajin:
            self.zoznamkrajin.add(nazov)
            self.uzly[nazov] = Uzol(nazov)
        self.uzly[nazov].pridajzaznam(Zaznam(zaznam))

    def hladaj(self, text):
        self.strom.itervalues(prefix=text)

    def spravstrom(self):
        for i in self.uzly:
            self.strom[i.lower()] = self.uzly[i]
