from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qt_material
from pygame import mixer
from os import path , chdir,listdir,walk,scandir
from sys import argv,exit
from add_folder import addfolder
from pyqt_music_player_widget import MusicPlayerWidget
from PyQt5.QtMultimedia import QMediaPlayer,QMediaContent,QMediaPlaylist,QAudioOutput
import mutagen
from threading  import Thread



FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"GUI/player.ui"))


class mainapp(QMainWindow,FORM_CLASS):
	def __init__(self, parent=None):
		super(mainapp,self).__init__(parent)
		QMainWindow.__init__(self)
		self.setupUi(self)
		
		self.initalize()
		self.filetreeinit()
		self.button_setup()
	
	def initalize(self):
		mixer.init()
		self.player = mixer.music
		self.addfolder = addfolder()
		self.pause_bt.hide()
		self.qplayer = QMediaPlayer()
		currvol = self.player.get_volume()
		print(currvol)
		self.volume_bar.setValue(int(currvol*100))

	def playaudiofile(self,filepath):
		url = QUrl.fromLocalFile(filepath)
		content = QMediaContent(url)
		self.qplayer.setMedia(content)
		self.qplayer.play()

	def button_setup(self):
		self.add_bt.clicked.connect(self.addfolderwin)
		self.addfolder.add_bt.clicked.connect(self.addfolder.add_path)
		self.addfolder.add_bt.clicked.connect(self.filetreeinit)
		self.treeWidget.itemClicked.connect(self.play)
		self.pause_bt.clicked.connect(self.pause)
		self.play_bt.clicked.connect(self.resume)
		self.volume_bar.valueChanged.connect(self.volume)

	def addfolderwin(self):
		self.addfolder.show()

	def filetreeinit(self):
		self.treeWidget.clear()
		songs = []
		with open("dirs.txt","r") as f:
			self.x = f.readlines()
			print(self.x)
			i = 0
			self.song_dict = {}
			for (dirp,dirn,file) in walk(self.x[0].strip()):
				if dirn == [] :
					if file !=[]:
						files = []
						for songaya in file:
							if songaya[-1] == "3":
								files.append(songaya)
						songs.append(files)
						songs[i].append(dirp)
						i+=1

		
			i = 0
			for artist in songs:
				try:
					# audios = mutagen.mp3.MP3(f"{artist[-1]}\\{artist[0]}",ID3=mutagen.easyid3.EasyID3)
					item0 = QTreeWidgetItem(self.treeWidget)
					myind = artist[-1].find("\\")
					self.treeWidget.topLevelItem(i).setText(0,artist[-1][myind+1:])
					x = 0
				except:
					# print(f"{artist[-1]}\\{artist[0]}")
					continue
				for song in artist:
					if song[-1] =="3":
						try:
							audio = mutagen.mp3.MP3(f"{artist[-1]}\\{song}",ID3=mutagen.easyid3.EasyID3)
							# print(audio['title'][0])
							self.song_dict[audio['title'][0]] = song
							item1 = QTreeWidgetItem(item0)
							s = audio['title'][0]
							
							self.treeWidget.topLevelItem(i).child(x).setText(0,s)
							# self.treeWidget.topLevelItem(i).child(x).setText(0,song)

							x+=1
							# print(audio['artist'][0])
						except:
							continue
				i+=1

	def play(self,it,col):
		try:
			parnt = it.parent().text(col)
			if parnt != None:
				selected = it.text(col)
				y = 0
				for i in range(len(self.x)):
					try:
						# self.playaudiofile(fr"{self.x[y].strip()}\\{parnt}\\{self.song_dict[selected]}" )
						print(self.song_dict[selected])

						self.player.load(fr"{self.x[y].strip()}\\{parnt}\\{self.song_dict[selected]}")
						self.player.play()
						# self.thread()
						self.timebar_man(fr"{self.x[y].strip()}\\{parnt}\\{self.song_dict[selected]}")
						self.song_title.setText(selected)
						self.song_artist.setText(parnt)
						self.pause_bt.show()
					except Exception as e:
						print(e)
						y +=1
						continue
		except Exception as e:
			# print(self.treeWidget.isExpanded(it))
			self.treeWidget.expandItem(it)

	def timebar_man(self,song):
		song_len = mutagen.mp3.MP3(song).info.length
		songi = song_len/60
		songindx = str(songi).find(".")
		self.song_time.setText(f"{str(songi)[:songindx]}:{int(float(str(songi)[songindx:])*60)}")


	def pause(self):
		self.player.pause()
		
		self.pause_bt.hide()
		self.play_bt.show()

	def resume(self):
		self.player.unpause()
		self.thread()
		self.play_bt.hide()
		self.pause_bt.show()

	def volume(self):
		newvol = self.volume_bar.value()
		self.player.set_volume(float(newvol/100))
		print(float(newvol/100))

	def time(self):
		while self.player.get_busy() == True:
			print(self.player.get_pos()/1000)

	def thread(self):
		t1 = Thread(target=self.time)
		t1.start()

if __name__ == "__main__":
  app = QApplication(argv)
  MainWindow = QMainWindow()
  window = mainapp()
  window.show()
  exit(app.exec_())
