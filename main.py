from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from index import index

from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
# from kivy.uix.spinner import Spinner
# from kivy.uix.button import Button
# from kivy.uix.label import Label

class vsetko(FloatLayout):
    orientation = 'vertical'
    global pole

    def zozenzoznam(self):
        oznam = self.ids["stavzoznamumap"]
        priecinok = self.ids["priecinok"]
        postupstahovania = Popup(title='Stahujem zoznamy', auto_dismiss=False)
        progresbar = ProgressBar(max=128)
        postupstahovania.add_widget(progresbar)
        self.add_widget(postupstahovania)
        stavzoznamu = self.ids["stavzoznamumap"]

        def kolbek(blocks, block_size, total_size):
            progresbar.value = blocks
        self.index = index()

        def dostahovane():
            self.remove_widget(progresbar)
            postupstahovania.text = "Spracovavam zoznamy"
            def koniec():
                self.remove_widget(postupstahovania)
                stavzoznamu.text = "Zoznam map je aktualny"
            self.index.spravstrom(koniec)
        self.index.stiahnizoznam(kolbek, dostahovane)



    def vybertyp(self, **args):
        global pole
        vyberkoninentu = self.ids["vyberkontinent"]
        vybertypu = self.ids["vybertyp"]
        text = vybertypu.text
        for i in pole[text]:
            vyberkoninentu.values.append(i)

    def vyberkontinent(self, **args):
        global pole
        vyberkontinentu = self.ids["vyberkontinent"]
        vyberkrajiny = self.ids["vyberkrajinu"]
        vybertypu = self.ids["vybertyp"]
        typ = vybertypu.text
        kontinent = vyberkontinentu.text
        for i in pole[typ][kontinent]:
            vyberkrajiny.values.append(i)


class main(App):
    def build(self):
        return vsetko()


if __name__ == "__main__":
    main().run()
