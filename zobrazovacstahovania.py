from kivy.uix.popup import Popup


class ZobrazovacStahovania(Popup):

    def __init__(self, **kwargs):
        super(ZobrazovacStahovania, self).__init__(**kwargs)
        self._suborov = 0
        self._stiahnutych = 0
        self.velkost = 0
        self.blokov = 0
        self.velkostbloku = 0
        self._stiahnutychblokov = 0
        self.subory = self.ids.subory
        self.percenta = self.ids.percenta
        self.progresbar = self.ids.progressbar

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
    def stiahnutychblokov(self):
        return self._stiahnutych

    @stiahnutychblokov.setter
    def stiahnutychblokov(self, sblokov):
        self._stiahnutychblokov = sblokov
        self.progresbar.max = int(self.velkost/self.velkostbloku)
        self.progresbar.value = sblokov

    @property
    def suborov(self):
        return self._suborov

    @suborov.setter
    def suborov(self, suborov):
        self._suborov = suborov
        self.nastavsubory()
