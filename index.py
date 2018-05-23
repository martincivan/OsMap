import xml.etree.ElementTree
from urllib.request import urlretrieve
import threading
from typ import typ


class Index:
    adresa = 'http://download.osmand.net/get_indexes.php'
    meno = 'zoznam.xml'
    kam = ''
    zoznamtypov = ['hillshade', 'map', 'wikimap', 'wikivoyage', 'voice', 'fonts', 'depth', 'road_map', 'srtm_map', 'region']
    typy = {}

    def __init__(self):
        for t in self.zoznamtypov:
            self.typy[t] = typ(t)

    def stiahnizoznam(self, kolbek, koniec):
        self.odkial = self.kam+self.meno

        def makaj():
            # urlretrieve(self.adresa, self.kam + self.meno, kolbek)
            koniec()
        vlakno = threading.Thread(target=makaj)
        vlakno.start()

    def spravstrom(self, koniec):
        def makaj():
            self.strom = xml.etree.ElementTree.parse(self.odkial)
            self.koren = self.strom.getroot()
            self.spravzoznamy()
            koniec()
        vlakno = threading.Thread(target=makaj)
        vlakno.start()


    def spravzoznamy(self):
        for dieta in self.koren:
            try:
                #print("Pridavam: "+dieta.attrib['type'])
                self.typy[dieta.attrib['type']].pridajzaznam(dieta)
            except KeyError as inst:
                print("KeyError:"+str(inst))
