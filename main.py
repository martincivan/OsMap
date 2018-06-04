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
from zobrazenie import Zobrazenie


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
                vybertypu.data = [{"datum" : "datum",
                                "ikona" : "ikony/icon.png",
                                "nadpis" : str(x),
                                "popis" : "Redkovka " + str(x),
                                "pri_vybere" : self.vybertyp,
                                "typ" : str(x),
                                "velkost" : "velkost", 
                                "zaznam" : x} for x in self.index.typy]
            self.index.spravstrom(koniec)
        self.index.stiahnizoznam(kolbek, dostahovane)


    def vybertyp(self, *args):
        print("Vybral som")
        vyberkoninentu = self.ids["vyberkontinent"]
        self.vybraty_typ = args[0]
        print("Vybrate: " + self.vybraty_typ)
        t = self.index.typy[self.vybraty_typ]
        vyberkoninentu.data = [{"datum" : "datum",
                                "ikona" : "ikony/icon.png", 
                                "nadpis" : str(x), 
                                "popis" : "Redkovka " + str(x), 
                                "pri_vybere" : self.vyberkontinent,
                                "typ" : str(x),
                                "velkost" : "velkost" } for x in t.zoznamkontinentov]
       
    def vyberkontinent(self, *args):
        vyberkrajiny = self.ids["vyberkrajinu"]
        t = self.index.typy[self.vybraty_typ]
        k = t.kontinenty[args[0]]
        lejaut_krajin = self.ids["lejaut_krajin"]
        
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
