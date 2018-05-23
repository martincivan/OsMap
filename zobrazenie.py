from index import Index
from kivy.uix.listview import ListItemButton
from kivy.uix.listview import SelectableView
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.app import App

class SelectableRecycleBoxLayout(LayoutSelectionBehavior, RecycleBoxLayout):
    pri_vybere = None
    vybrate = None
    


class Zobrazenie(RecycleDataViewBehavior, BoxLayout):
    typ = StringProperty()
    ikona = StringProperty()#"ikony/icon.png"
    nadpis = StringProperty()#"Redkovka"
    popis = StringProperty()#"Toto je barjaka redkovka"
    datum = StringProperty()#"9.6.2017"
    velkost = StringProperty()#"37 cm"
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    pri_vybere = None

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(Zobrazenie, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(Zobrazenie, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            #print("selection changed to {0}".format(rv.data[index]))
            # self.parent.vybrate = rv.data[index]
            self.pri_vybere(rv.data[index]["typ"])
        else:
            #print("selection removed for {0}".format(rv.data[index]))
            pass

