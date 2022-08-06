from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QMainWindow,QApplication,QFileDialog
from os import path
from sys import argv

FORM_CLASS,_=loadUiType(path.join(path.dirname(__file__),"GUI/Addfile.ui"))

class addfolder(QMainWindow,FORM_CLASS):
	def __init__(self, parent=None):
		super(addfolder,self).__init__(parent)
		QMainWindow.__init__(self)
		self.setupUi(self)
		self.browse_bt.clicked.connect(self.browse)
	def add_path(self):
		with open("dirs.txt","a") as f:
			f.writelines(f"{self.path_input.text()}\n")
			self.path_input.setText("")

	def browse(self):
		path = QFileDialog.getExistingDirectory(self,'open a folder')
		self.path_input.setText(path)


		self.path_input.text()

if __name__ == "__main__":
  app = QApplication(argv)
  MainWindow = QMainWindow()
  window = addfolder()
  window.show()
  exit(app.exec_())
