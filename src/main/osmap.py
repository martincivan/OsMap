from kivy.config import ConfigParser
import xml.etree.ElementTree
from urllib.request import urlretrieve
import threading
from pathlib import Path
from src.main.index import Index

class Osmap:

    konfig=ConfigParser()
    index=Index()

    def nacitajnastavenia(self):
        konfig_cesta = Path('nastavenia/nastavenia.ini')
        konfig_json_cesta = Path('nastavenia/nastavenia.json')
        if konfig_cesta.is_file() and konfig_json_cesta.is_file():
            self.konfig.read('nastavenia/nastavenia.ini')
            direktoria = Path(self.konfig.get('Hlavne', 'priecinok'))
            if not direktoria.exists():
                self.konfig.set('Hlavne', 'priecinok', Path.home())
        else:
            raise FileNotFoundError

    def stiahnizoznam(self, kolbek, koniec):

        def makaj():
            adresa = self.konfig.get('Hlavne', 'adresazoznamov')
            self.kam = self.konfig.get('Hlavne', 'priecinok') + self.konfig.get('Hlavne', 'menozoznamov')
            # urlretrieve(adresa, self.kam , kolbek)
            koniec()
        vlakno = threading.Thread(target=makaj)
        vlakno.start()

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
