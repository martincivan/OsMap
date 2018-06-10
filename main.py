from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from index import Index
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.settings import SettingsWithTabbedPanel
from zobrazenie import Zobrazenie
from osmap import Osmap



class Vsetko(FloatLayout):
    orientation = 'vertical'
    global pole
    sceny = {}

    def zozenzoznam(self):
        postupstahovania = Popup(title='Stahujem zoznamy', auto_dismiss=False, size_hint=(.5, .3), pos_hint={'center': (.5, .5)})
        progresbar = ProgressBar(max=128)
        postupstahovania.add_widget(progresbar)
        self.add_widget(postupstahovania)
        stavzoznamu = self.ids["stavzoznamumap"]

        def kolbek(blocks, block_size, total_size):
            progresbar.value = blocks

        def dostahovane():
            self.remove_widget(progresbar)

            def koniec():
                self.remove_widget(postupstahovania)
                stavzoznamu.text = "Zoznam map je aktualny"
                hladaj = self.ids["hladaj"]
                hladaj.disabled = False
            Main.osmap.spravstrom(koniec)
        Main.osmap.stiahnizoznam(kolbek, dostahovane)

    def hladaj(self):
        vstup = self.ids["hladaj"]
        text = vstup.text
        if len(text) > 2:
            print("Hladaj: "+text)
            vysledok = Main.osmap.index.hladaj(text)
            if vysledok is not None:
                vyberkrajinu = self.ids["vyberkrajinu"]
                vyberkrajinu.data = [{"datum" : "datum",
                                    "ikona" : "ikony/icon.png",
                                    "nadpis" : str(x),
                                    "popis" : "Redkovka " + str(x.nazov),
                                    "pri_vybere" : self.vybertyp,
                                    "typ" : str(x),
                                    "velkost" : "velkost",
                                    "zaznam" : x.nazov} for x in vysledok]

    def vybertyp(self, *args):
        print("Vybral som")
        vyberkoninentu = self.ids["vyberkontinent"]
        self.vybraty_typ = args[0]
        print("Vybrate: " + self.vybraty_typ)
        t = self.index.typy[self.vybraty_typ]
        vyberkoninentu.data = [{"datum": "datum",
                                "ikona": "ikony/icon.png",
                                "nadpis": str(x),
                                "popis": "Redkovka " + str(x),
                                "pri_vybere": self.vyberkontinent,
                                "typ": str(x),
                                "velkost": "velkost"} for x in t.zoznamkontinentov]
       
    def vyberkontinent(self, *args):
        vyberkrajiny = self.ids["vyberkrajinu"]
        t = self.index.typy[self.vybraty_typ]
        k = t.kontinenty[args[0]]
        
        for x in range(len(vyberkrajiny.data)):
            vyberkrajiny._layout_manager.deselect_node(x)
            
        vyberkrajiny.data = [{"datum" : "datum", 
                            "ikona" : "ikony/icon.png", 
                            "nadpis" : x.pekny_nazov(), 
                            "popis" : "Subor: " + x.nazov, 
                            "pri_vybere" : self.vyberkrajinu, 
                            "typ" : str(x),
                            "velkost" : "velkost" } for x in sorted(k.zaznamy, key = lambda zaznam: zaznam.pekny_nazov())]

    def vyberkrajinu(self, *args):
        pass
    
    def nastav_obrazovku(self, obrazovka):
        obrazovky = self.ids["obrazovky"]
        obrazovky.current = obrazovka
        nazad = self.ids["nazad"]
        if obrazovka == "hlavna":
            nazad.title = "OsMap"
        else:
            nazad.title = "OsMap - " + obrazovka

    def spravnastavenia(self):
        if 'nastavenia' not in self.sceny:
            nastavenia = SettingsWithTabbedPanel()
            nastavenia.bind(on_close=(lambda l: self.nastav_obrazovku("hlavna")))
            lejaut = self.ids["lejaut_nastaveni"]
            nastavenia.add_json_panel("Hlavne", Main.osmap.konfig, "nastavenia/nastavenia.json")
            lejaut.add_widget(nastavenia)
            self.sceny['nastavenia'] = nastavenia
        self.nastav_obrazovku('nastavenia')


class Chyba(FloatLayout):
    orientation = 'vertical'
    
    def nasatv_spravu(self, sprava):
        label = self.ids['sprava']
        label.text = label.text % sprava
        

class Main(App):

    osmap=Osmap()

    def build(self):
        self.title='OsMap'
        self.icon='ikony/icon.png'
        try:
            self.osmap.nacitajnastavenia()
            self.sceny = set()
            return Vsetko()
        except FileNotFoundError:
            chyba = Chyba()
            chyba.nasatv_spravu('Nepodarilo sa najst konfiguraciu.')
            return chyba


if __name__ == "__main__":
    Main().run()
