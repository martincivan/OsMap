from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.settings import SettingsWithTabbedPanel
from src.main.osmap import Osmap
from src.gui.zobrazenie import Zobrazenie
from kivy.uix.recycleview import RecycleView
from kivy.properties import BooleanProperty



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
            try:
                vysledok = Main.osmap.index.hladaj(text)
                if vysledok is not None:
                    vyberkrajinu = self.ids["vyberkrajinu"]
                    vyberkrajinu.data = [{"ikona" : "ikony/icon.png",
                                        "nadpis" : str(x),
                                        "popis" : "Redkovka " + str(x.nazov),
                                        "pri_vybere" : self.vyberkrajinu,
                                        "uzol" : x} for x in vysledok]
            except KeyError:
                vyberkrajiny = self.ids["vyberkrajinu"]
                vyberkrajiny.data = [{"datum": "datum",
                                      "ikona": "ikony/ne.png",
                                      "nadpis": "Nic som nenasiel",
                                      "popis": "Ozaj nic",
                                      "selectable": BooleanProperty(False)}]

    def vyberkrajinu(self, *args):
        vybertypu = self.ids["vybertypu"]
        vybertypu.data = [{
            "datum": j.cas,
            "nadpis": i,
            "velkost": j.velkost
        } for i, j in args[0]["uzol"].zaznamy]

    
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
