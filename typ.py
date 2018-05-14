from kontinent import Kontinent
import re

class typ:
    zoznamkontinentov = ["Europe", "Asia"]

    def __init__(self, t):
        self.nazov = t
        self.kontinenty = {}
        for zkont in self.zoznamkontinentov:
            self.kontinenty[zkont] = Kontinent(zkont)

    def pridajzaznam(self, z):
        try:
            #print("Pridavam zaznam pre typ: {0} zaznam: {1}".format(self.nazov, z.attrib))
            nazov = z.attrib['name']
            kont = None
            for k in self.zoznamkontinentov:
                je = re.search(k.lower(), nazov.lower())
                if je:
                    kont = k
            if kont:
                print("Pridavam pre typ: {0}, kontinent: {1}, zaznam: {2}".format(self.nazov, kont, str(z.attrib)))
                self.kontinenty[kont].pridajzaznam(z)
        except KeyError as inst:
            print("KeyError"+str(inst))
