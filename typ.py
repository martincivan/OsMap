from kontinent import Kontinent
import re

class typ:
    zoznamkontinentov = ["Europe", "Asia", "South America", "North America", "Africa", "Australia"]

    def __init__(self, t):
        self.nazov = t
        self.kontinenty = {}
        for zkont in self.zoznamkontinentov:
            self.kontinenty[zkont] = Kontinent(zkont)

    def pridajzaznam(self, z):
        try:
            nazov = z.attrib['name']
            kont = None
            for k in self.zoznamkontinentov:
                je = re.search(k.lower().replace(' ',''), nazov.lower())
                if je:
                    kont = k
            if kont:
                self.kontinenty[kont].pridajzaznam(z)
        except KeyError as inst:
            print("KeyError"+str(inst))
