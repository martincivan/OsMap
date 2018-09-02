from threading import Thread
from urllib import urlretrieve
from zipfile import ZipFile
from pathlib import Path


class Stahovac():

    def __init__(self, co, zobrazovac, pokracovanie, konfig):
        self.co = co
        self.zobrazovac = zobrazovac
        self.pokracovanie = pokracovanie
        self.stiahnute = []
        self.konfig = konfig

    def kolbekStahovania(self, blocks, block_size, total_size):
        self.zobrazovac.velkostbloku = block_size
        self.zobrazovac.velkost = total_size
        self.zobrazovac.stiahnutychblokov = blocks

    def dostahovane(self):
        self.zobrazovac.dismiss()

    def stiahni(self):
        def makaj():
            while len(self.stiahnute) < len(self.co):
                nieco = self.co[len(self.stiahnute)]
                adresa = str(self.konfig.get('Hlavne', 'adresasuborov') + nieco.subor)
                self.kam = Path(self.konfig.get('Priecinky', 'p_' + nieco.typ)) / Path(nieco.subor)
                urlretrieve(adresa, str(self.kam), self.kolbekStahovania)
                self.stiahnute.append(nieco)

                def posun():
                    self.zobrazovac.stiahnutych = len(self.stiahnute)
                    nazov = Path(nieco.subor)
                    print(nazov.suffix)
                    if nazov.suffix == '.zip':
                        zip = ZipFile(str(self.kam), 'r')
                        zip.extractall(str(self.konfig.get('Priecinky', 'p_' + nieco.typ)))
                        zip.close()

                posunutie = Thread(target=posun())
                posunutie.start()
            self.dostahovane()

        vlakno = Thread(target=makaj)
        vlakno.start()
