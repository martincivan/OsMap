from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.settings import SettingsWithTabbedPanel
from osmap.osmap import Osmap
from kivy.properties import BooleanProperty
from kivy.properties import ListProperty
from zobrazenie import Zobrazenie


class Vsetko(FloatLayout):
    orientation = 'vertical'
    global pole
    sceny = {}
    na_stiahnutie = ListProperty()

    def zozenzoznam(self):
        postupstahovania = Popup(title='Stahujem zoznamy', auto_dismiss=False, size_hint=(.5, .3),
                                 pos_hint={'center': (.5, .5)})
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
            print("Hladaj: " + text)
            try:
                vysledok = Main.osmap.index.hladaj(text)
                if vysledok is not None:
                    vyberkrajinu = self.ids["vyberkrajinu"]
                    vyberkrajinu.layout_manager.clear_selection()
                    vyber_typu_acc = self.ids["vyber_typu_acc"]
                    vyber_typu_acc.disabled = True
                    vyberkrajinu.data = [{"datum": "",
                                          "ikona": "ikony/default/",
                                          "nadpis": str(x),
                                          "popis": "Redkovka " + str(x.nazov),
                                          "pri_vybere": self.vyberkrajinu,
                                          "uzol": x} for x in vysledok]
            except KeyError:
                vyber_typu_acc = self.ids["vyber_typu_acc"]
                vyber_typu_acc.disabled = True
                vyberkrajiny = self.ids["vyberkrajinu"]
                vyberkrajiny.data = [{"datum": "",
                                      "ikona": "ikony/ne/",
                                      "nadpis": "Nic som nenasiel",
                                      "popis": "Skus zadat skutocny nazov krajiny ty expert",
                                      "pri_vybere": None,
                                      "uzol": None}]
                vyberkrajiny.layout_manager.deselect_node(0)

    def vyberkrajinu(self, *args):
        vybertypu = self.ids["vybertypu"]
        vybertypu.data = [{
            "datum": j.datum,
            "ikona": j.miesto_ikony(),
            "nadpis": i,
            "popis": j.popis,
            "pri_vybere": self.vyber_subor,
            "pri_zruseni": self.zrus_subor,
            "velkost": j.mbsuboru + ' MB',
            "zaznam": j
        } for i, j in args[0]["uzol"].zaznamy]

        for node in range(len(vybertypu.data)):
            if vybertypu.data[node]["zaznam"] in self.na_stiahnutie:
                vybertypu.layout_manager.select_node(node)
            else:
                vybertypu.layout_manager.deselect_node(node)

        vyber_typu_acc = self.ids["vyber_typu_acc"]
        vyber_typu_acc.disabled = False
        vyber_typu_acc.collapse = False

    def vyber_subor(self, vybraty):
        self.na_stiahnutie.append(vybraty["zaznam"])

    def zrus_subor(self, zruseny):
        self.na_stiahnutie.remove(zruseny["zaznam"])

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
            nastavenia.add_json_panel("Hlavne", Main.osmap.konfig, str(Main.osmap.konfig_json_cesta))
            nastavenia.add_json_panel("Priecinky", Main.osmap.konfig, str(Main.osmap.konfig_json_priecinky))
            lejaut.add_widget(nastavenia)
            self.sceny['nastavenia'] = nastavenia
        self.nastav_obrazovku('nastavenia')


class Chyba(FloatLayout):
    orientation = 'vertical'

    def nasatv_spravu(self, sprava):
        label = self.ids['sprava']
        label.text = label.text % sprava


class Main(App):
    osmap = Osmap()

    def build(self):
        self.title = 'OsMap'
        self.icon = 'ikony/icon.png'
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
