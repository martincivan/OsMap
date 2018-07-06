from pygtrie import CharTrie
from uzol import Uzol
from zaznam import Zaznam
from babel import Locale
import babel.core
import pycountry

class Index:

    def __init__(self):
        self.zoznamkrajin = set()
        self.uzly = {}
        self.strom = CharTrie()
        self.strom.enable_sorting(enable=True)


    def pridajzaznam(self, zaznam):
        name = zaznam.attrib['name'].split("_")
        typ = zaznam.attrib['type']
        nazov = ''

        if typ == 'hillshade':
            name.remove(name[0])
            nazov = name[0]

        elif typ == 'voice':
            jazyk = name[0].split('-')[0]
            try:
                lokale = Locale.parse(babel.core.LOCALE_ALIASES[jazyk])
                nazov = lokale.get_territory_name(Locale('en'))

            except KeyError:
                print('Nerozoznal som skratku jazyka: ' + jazyk)
                nazov = 'Voice ' + jazyk

            print(nazov)

        else:
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
