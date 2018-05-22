from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from index import Index
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.config import ConfigParser
from pathlib import Path
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton


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
            def koniec():
                self.remove_widget(postupstahovania)
                stavzoznamu.text = "Zoznam map je aktualny"
                vybertypu = self.ids["vybertyp"]
                konvertor = lambda row_index, rec: {'text': rec,
                                         'size_hint_y': None,
                                         'height': 25}
                adapter = ListAdapter(data=self.index.typy, args_converter=konvertor, cls=ListItemButton, selection_mode='single', allow_empty_selection=False)
                adapter.bind(on_selection_change=self.vybertyp)
                vybertypu.adapter = adapter
            self.index.spravstrom(koniec)
        self.index.stiahnizoznam(kolbek, dostahovane)


    def vybertyp(self, vyber):
        print("Vybral som")
        vyberkoninentu = self.ids["vyberkontinent"]
        text = vyber.selection[0]
        print("Vybrate: " + text.text)
        t = self.index.typy[text.text]
        konvertor = lambda row_index, rec: {'text': rec,
                                         'size_hint_y': None,
                                         'height': 25}
        vyberkoninentu.adapter = ListAdapter(data=t.zoznamkontinentov, args_converter=konvertor, cls=ListItemButton, selection_mode='single', allow_empty_selection=False)

    def vyberkontinent(self, **args):
        vyberkontinentu = self.ids["vyberkontinent"]
        vyberkrajiny = self.ids["vyberkrajinu"]
        vybertypu = self.ids["vybertyp"]
        ty = vybertypu.text
        kont = vyberkontinentu.text
        t = self.index.typy[ty]
        k = t.kontinenty[kont]
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
        
class Chyba(FloatLayout):
    orientation = 'vertical'
    
    def nasatv_spravu(self, sprava):
        label = self.ids['sprava']
        label.text = label.text % sprava
        

        
    
        
class Main(App):

    konfig=ConfigParser()

    def build(self):
        self.title='OsMap'
        self.icon='ikony/icon.png'
        konfig_cesta = Path('nastavenia/nastavenia.ini')
        konfig_json_cesta = Path('nastavenia/nastavenia.json')
        if konfig_cesta.is_file() and konfig_json_cesta.is_file():
            self.konfig.read('nastavenia/nastavenia.ini')
            direktoria = Path(self.konfig.get('Hlavne', 'priecinok'))
            if not direktoria.exists():
                self.konfig.set('Hlavne', 'priecinok', Path.home())
            self.sceny = set()
            return Vsetko()
        else:
            chyba = Chyba()
            chyba.nasatv_spravu('Nepodarilo sa najst konfiguraciu.')
            return chyba


if __name__ == "__main__":
    Main().run()
