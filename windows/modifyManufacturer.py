
from PyQt5.QtWidgets import QLineEdit

from PyQt5 import QtCore

from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton


class modifyManufacturerWindow(QWidget):
    path=""
    modifyElementSignal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(modifyManufacturerWindow, self).__init__(parent)
        self.setup()

    def getData(self, data):
        self.path = data

    def setText(self, manufacturer):
        if manufacturer != "Nie dodano jeszcze tej zawartości":
            self.manufacturertWindow.setText(manufacturer)

    def sendData(self):
        self.modifyElementSignal.emit(self.manufacturertWindow.text())
        self.close()

    def exit(self):
        self.close()

    def setup(self):
        self.manufacturerText = QLabel('Wydawca: ', self)
        self.manufacturertWindow = QLineEdit()


        self.applyBotton = QPushButton("Zatwierdz", self)
        self.applyBotton.clicked.connect(self.sendData)

        self.exitButton = QPushButton("Anuluj", self)
        self.exitButton.clicked.connect(self.exit)

        layout = QGridLayout()
        layout.addWidget(self.manufacturerText, 0, 0)
        layout.addWidget(self.manufacturertWindow, 0, 1)
        layout.addWidget(self.applyBotton, 0, 2)
        layout.addWidget(self.exitButton, 1, 2)

        self.setLayout(layout)
        self.setWindowTitle("modyfikuj")
        self.show()