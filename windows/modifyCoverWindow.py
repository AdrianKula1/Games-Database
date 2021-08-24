from shutil import copyfile
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLineEdit, QFileDialog, QMessageBox
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton



class modifyCoverWindow(QWidget):
    modifyElementSignal = QtCore.pyqtSignal(str)
    destPath=""
    def __init__(self, parent=None):
        super(modifyCoverWindow, self).__init__(parent)
        self.setup()

    def setText(self, data):
        if data != "Nie dodano jeszcze tej zawartości":
            self.destPath=data
            self.coverPath.setText(data)


    def uploadImage(self):
        self.file = QFileDialog.getOpenFileName(self, 'open file', 'c\\', 'image files(*.jpg)')
        self.sourcePath = self.file[0]
        self.coverPath.setText(self.sourcePath)



    def sendData(self):
        copyfile(self.sourcePath, self.destPath)
        self.modifyElementSignal.emit("-1")
        self.close()


    def exit(self):
        self.close()
        pass

    def setup(self):

        self.coverText = QLabel('Okładka: ', self)
        self.coverPath = QLineEdit()
        self.coverButton = QPushButton("...")
        self.coverButton.clicked.connect(self.uploadImage)

        self.applyButton = QPushButton("Zatwierdź", self)
        self.applyButton.clicked.connect(self.sendData)

        self.exitButton = QPushButton("Anuluj", self)
        self.exitButton.clicked.connect(self.exit)

        layout = QGridLayout()
        layout.addWidget(self.coverText, 0, 0)
        layout.addWidget(self.coverPath, 0, 1)
        layout.addWidget(self.coverButton, 0, 2)
        layout.addWidget(self.applyButton, 0, 3)
        layout.addWidget(self.exitButton, 1, 3)

        self.setLayout(layout)
        self.setWindowTitle("modyfikuj")
        self.show()