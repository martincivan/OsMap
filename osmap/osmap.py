from kivy.config import ConfigParser
import xml.etree.ElementTree
import threading
from pathlib import Path
import os.path
from datetime import datetime
from osmap.index import Index


class Osmap:
    konfig = ConfigParser()
    index = Index()

    def nacitajnastavenia(self):
        konfig_cesta = Path('nastavenia/nastavenia.ini')
        self.konfig_json_cesta = Path('nastavenia/nastavenia.json')
        self.konfig_json_priecinky = Path('nastavenia/nastavenia_priecinkov.json')
        if konfig_cesta.is_file() and self.konfig_json_cesta.is_file() and self.konfig_json_priecinky:
            self.konfig.read(str(konfig_cesta))
            direktoria = Path(self.konfig.get('Hlavne', 'priecinok'))
            if not direktoria.exists():
                self.konfig.set('Hlavne', 'priecinok', Path('').resolve())
                self.konfig.write()
        else:
            raise FileNotFoundError

    def stiahnizoznam(self, kolbek, koniec, stiahnut=False):

        def makaj():
            adresa = self.konfig.get('Hlavne', 'adresazoznamov')
            self.kam = Path(self.konfig.get('Hlavne', 'priecinok')) / Path(self.konfig.get('Hlavne', 'menozoznamov'))
            frekv_stahovania_zoznamu = self.konfig.get('Hlavne', 'frekvencia_stahovania_zoznamu')
            if stiahnut or not self.kam.exists() or (self.dni_zoznamu() > int(frekv_stahovania_zoznamu) > 0):
                print('Stiahol by som novy zoznam')
                # urlretrieve(adresa, self.kam , kolbek)
            koniec()

        vlakno = threading.Thread(target=makaj)
        vlakno.start()

    def dni_zoznamu(self):
        vek = datetime.now() - datetime.fromtimestamp(os.path.getmtime(str(self.kam)))
        return vek.days

    def spravstrom(self, koniec):
        # def makaj():
        self.strom = xml.etree.ElementTree.parse(self.kam)
        self.koren = self.strom.getroot()
        self.spravzoznamy()
        self.index.spravstrom()
        koniec()
        # vlakno = threading.Thread(target=makaj)
        # vlakno.start()

    def spravzoznamy(self):
        for dieta in self.koren:
            self.index.pridajzaznam(dieta)

    @property
    def typy(self):
        return list(self.index.zoznamtypov)
