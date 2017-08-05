from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
#from kivy.uix.spinner import Spinner
#from kivy.uix.button import Button
#from kivy.uix.label import Label
try:
	from urllib.request import urlretrieve
except:
	from urllib import urlretrieve

class vsetko(FloatLayout):
	orientation='vertical'
	global pole
	
	def zozenzoznam(self):
		oznam=self.ids["stavzoznamumap"]
		oznam.text='zhanam'
		priecinok = self.ids["priecinok"]
		urlretrieve('http://download.osmand.net/get_indexes.php', priecinok.text+'zoznam.xml')
		oznam.text='stiahnute'
		oznam.text='citam'
		f = open(priecinok.text+'zoznam.xml')
		riadky = f.readlines()
		del riadky[-1]
		del riadky[0]
		del riadky[0]
		global pole
		pole = {}
		pole["map"] = {}
		pole["voice"] = {}
		pole["wikimap"] = {}
		pole["road_map"] = {}
		pole["srtm_map"] = {}
		pole["hillshade"] = {}
		docasny = {}
		docasny["africa"] = {}
		docasny["asia"] = {}
		docasny["europe"] = {}
		docasny["southamerica"] = {}
		docasny["northamerica"] = {}
		docasny["centralamerica"] = {}
		docasny["australia-oceania"] = {}
		docasny["basemap"] = {}
		pole["map"]=docasny
		pole["voice"]=docasny
		pole["wikimap"]=docasny
		pole["road_map"]=docasny
		pole["srtm_map"]=docasny
		pole["hillshade"]=docasny
		
		for i in riadky:
			riadok = i[3:-3]
			#print(riadok)
			docasny = riadok.split()
			typ = docasny[1][6:-1]
			kontinent = docasny[-1][:-1].lower()
			if docasny[-2][0].isupper():
				krajina = docasny[-2]
			if docasny[-3][0].isupper():
				krajina = docasny[-3]
				j=0
				skuska=docasny[j][0:6]
			while skuska !='name="':
				j=j+1
				skuska=docasny[j][0:6]
			nazov=docasny[j][6:-1]
			#print(typ + " " + kontinent + " " + krajina + " " + nazov)	
			if typ == "voice":
				kontinent = "europe"
			
			if kontinent !="wiki" and kontinent!='description="':
				pole[typ][kontinent][krajina]=nazov
		#print(pole)
		oznam.text='precitane'	 
		vybertyp=self.ids["vybertyp"]
		for i in pole:
			vybertyp.values.append(i)
		
	def vybral(self, *args):
		print('vybral')


	def vybertyp(self, **args):
		global pole
		vyberkoninentu=self.ids["vyberkontinent"]
		vybertypu=self.ids["vybertyp"]
		text=vybertypu.text
		for i in pole[text]:
			vyberkoninentu.values.append(i)
	def vyberkontinent(self, **args):
		global pole
		vyberkontinentu=self.ids["vyberkontinent"]
		vyberkrajiny=self.ids["vyberkrajinu"]
		vybertypu=self.ids["vybertyp"]
		typ=vybertypu.text
		kontinent=vyberkontinentu.text
		for i in pole[typ][kontinent]:
			vyberkrajiny.values.append(i)
class main(App):
	def build(self):
		return vsetko()

if __name__=="__main__":
	main().run()
