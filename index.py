import xml.etree.ElementTree
from urllib.request import urlretrieve
import threading
from typ import typ


class index:
    adresa = 'http://download.osmand.net/get_indexes.php'
    meno = 'zoznam.xml'
    kam = ''
    zoznamTypov = ["hillshade", "map", "wikimap", "voice", "fonts", "depth", "road_map", "srtm_map"]
    typy = {}

    def __init__(self):
        for t in self.zoznamTypov:
            self.typy[t] = typ(t)

    def stiahnizoznam(self, kolbek, koniec):
        self.odkial = self.kam+self.meno
        def makaj():
            urlretrieve(self.adresa, self.kam + self.meno, kolbek)
            koniec()
        vlakno = threading.Thread(target=makaj)
        vlakno.start()

    def spravstrom(self, koniec):
        def makaj():
            self.strom = xml.etree.ElementTree.parse(self.odkial)
            self.koren = self.strom.getroot()
            koniec()
        vlakno = threading.Thread(target=makaj)
        vlakno.start()


    def spravzoznamy(self):
        for dieta in self.koren:
            self.typy[dieta.tag].pridajZaznam(dieta)
