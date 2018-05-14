from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from index import Index
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.config import ConfigParser


class Vsetko(FloatLayout):
    orientation = 'vertical'
    global pole
    sceny = {}

    def zozenzoznam(self):
        oznam = self.ids["stavzoznamumap"]
        priecinok = Main.konfig.get('Hlavne', 'priecinok')
        postupstahovania = Popup(title='Stahujem zoznamy', auto_dismiss=False, size_hint=(.5, .3), pos_hint={'center':(.5,.5)})
        progresbar = ProgressBar(max=128)
        postupstahovania.add_widget(progresbar)
        self.add_widget(postupstahovania)
        stavzoznamu = self.ids["stavzoznamumap"]

        def kolbek(blocks, block_size, total_size):
            progresbar.value = blocks
        self.index = Index()

        def dostahovane():
            self.remove_widget(progresbar)
            postupstahovania.text = "Spracovavam zoznamy"
            def koniec():
                self.remove_widget(postupstahovania)
                stavzoznamu.text = "Zoznam map je aktualny"
                vybertypu = self.ids["vybertyp"]
                for t in self.index.typy:
                    vybertypu.values.append(t)
                    print("Pridal som: "+t)
            self.index.spravstrom(koniec)
        self.index.stiahnizoznam(kolbek, dostahovane)



    def vybertyp(self, **args):
        vyberkoninentu = self.ids["vyberkontinent"]
        vybertypu = self.ids["vybertyp"]
        text = vybertypu.text
        t = self.index.typy[text]
        for k in t.zoznamkontinentov:
            vyberkoninentu.values.append(k)
            print("Pridavam: " + k)

    def vyberkontinent(self, **args):
        vyberkontinentu = self.ids["vyberkontinent"]
        vyberkrajiny = self.ids["vyberkrajinu"]
        vybertypu = self.ids["vybertyp"]
        ty = vybertypu.text
        kont = vyberkontinentu.text
        t = self.index.typy[ty]
        k = t.kontinenty[kont]
        print("MAM T: "+t.nazov)
        print("MAM K: "+k.nazov)
        print("POCET ZAZNAMOV: " + str(len(k.zaznamy)))
        for z in k.zaznamy:
        #    print("Pridavam: " + str(z.atrib))
            vyberkrajiny.values.append(z.nazov)
    
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
            nastavenia.add_json_panel("Hlavne", Main.konfig, "nastavenia/nastavenia.json")
            lejaut.add_widget(nastavenia)
            self.sceny['nastavenia'] = nastavenia
        self.nastav_obrazovku('nastavenia')


class Main(App):

    konfig=ConfigParser()

    def build(self):
        self.title='OsMap'
        self.konfig.read('nastavenia/nastavenia.ini')
        self.sceny = set()
        return Vsetko()


if __name__ == "__main__":
    Main().run()
