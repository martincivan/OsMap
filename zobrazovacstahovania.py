from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar


class ZobrazovacStahovania(Popup):

    def __init__(self):
        self.suborov = 0
        self._stiahnutych = 0
        self.velkost = 0
        self.blokov = 0
        self.velkostbloku = 0
        self._sblokov = 0
        self.subory = None
        self.percenta = None

    @property
    def stiahnutych(self):
        return self._stiahnutych

    def nastavsubory(self):
        self.subory.text = str(self.stiahnutych) + " / " + str(self.suborov)

    @stiahnutych.setter
    def stiahnutych(self, stiahnutych):
        self._stiahnutych = stiahnutych
        self.nastavsubory()

    @property
    def sblokov(self):
        return self._sblokov

    @sblokov.setter
    def sblokov(self, sblokov):
        self._sblokov = sblokov
        # self.percenta = ProgressBar()
        self.percenta.max = 100
        self.percenta.value = sblokov
