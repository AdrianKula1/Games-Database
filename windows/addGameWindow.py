import pathlib
from shutil import copyfile

from PyQt5 import QtCore
from PyQt5.QtWidgets import QLineEdit, QDateEdit, QFileDialog
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton

import gameClass
import globals

class addGameWindow(QWidget):
    addGameSignal = QtCore.pyqtSignal(gameClass.Game)
    destPath = None
    file = None
    def __init__(self, parent=None):
        super(addGameWindow, self).__init__(parent)
        self.setup()


    def exit(self):
        globals.gamesCounter-=1
        self.close()

    def sendData(self):
        self.destPath = self.destPath.replace("/", "\\")
        self.sourcePath = self.sourcePath.replace("/", "\\")
        copyfile(self.sourcePath, self.destPath)
        self.data = gameClass.Game(self.nameWindow.text(), self.destPath, self.dateedit.text().replace('.', '/'), self.manufacturertWindow.text())
        self.addGameSignal.emit(self.data)
        self.close()

    def uploadImage(self):
        globals.gamesCounter+=1
        self.file = QFileDialog.getOpenFileName(self, 'open file', 'c\\', 'image files(*.jpg)')
        self.sourcePath = self.file[0].replace("\windows", "")
        self.coverPath.setText(self.sourcePath)
        self.destPath = str(pathlib.Path(__file__).parent.absolute()).replace("\windows", "")
        self.destPath += "\images\image"
        self.destPath += str(globals.gamesCounter)
        self.destPath += ".jpg"

    def setup(self):
        self.nameText = QLabel('Nazwa gry: ', self)
        self.nameWindow = QLineEdit()

        self.coverText = QLabel('Okładka: ', self)
        self.coverPath = QLineEdit()
        self.coverButton = QPushButton("...")
        self.coverButton.clicked.connect(self.uploadImage)

        self.manufacturerText = QLabel('Wydawca: ', self)
        self.manufacturertWindow = QLineEdit()

        self.releaseDateText = QLabel('Data wydania:', self)
        self.dateedit = QDateEdit(calendarPopup=True)
        self.dateedit.setDateTime(QtCore.QDateTime.currentDateTime())

        self.applyBotton = QPushButton("Zatwierdz", self)
        self.applyBotton.clicked.connect(self.sendData)

        self.exitButton = QPushButton("Anuluj", self)
        self.exitButton.clicked.connect(self.exit)

        layout = QGridLayout()
        layout.setSpacing(6)
        layout.addWidget(self.nameText, 0, 0)
        layout.addWidget(self.nameWindow, 0, 1)
        layout.addWidget(self.coverText, 1, 0)
        layout.addWidget(self.coverPath, 1, 1)
        layout.addWidget(self.coverButton, 1, 2)
        layout.addWidget(self.manufacturerText, 2, 0)
        layout.addWidget(self.manufacturertWindow, 2, 1)
        layout.addWidget(self.releaseDateText, 3, 0)
        layout.addWidget(self.dateedit, 3, 1)
        layout.addWidget(self.applyBotton, 0, 5)
        layout.addWidget(self.exitButton, 1, 5)

        self.setLayout(layout)
        self.setWindowTitle("Dodaj grę")
        self.show()

