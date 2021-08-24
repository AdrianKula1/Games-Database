
from PyQt5.QtWidgets import QLineEdit, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton

class modifyRateWindow(QWidget):
    path=""
    modifyElementSignal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(modifyRateWindow, self).__init__(parent)
        self.setup()

    def setText(self, data):
        if data != "Nie dodano jeszcze tej zawartości" and data is not None:
            self.rateWindow.setText(data)

    def sendData(self):
        if int(self.rateWindow.text()) in range(0, 11):
            self.modifyElementSignal.emit(self.rateWindow.text())
            self.close()
        else:
            QMessageBox.information(self, "", "Proszę wpisać liczbę z zakresu 0-10", QMessageBox.Ok)

    def exit(self):
        self.close()

    def setup(self):

        self.rateText = QLabel('Ocena (0-10): ', self)
        self.rateWindow = QLineEdit()

        self.applyButton = QPushButton("Zatwierdz", self)
        self.applyButton.clicked.connect(self.sendData)

        self.exitButton = QPushButton("Anuluj", self)
        self.exitButton.clicked.connect(self.exit)

        layout = QGridLayout()
        layout.addWidget(self.rateText, 0, 0)
        layout.addWidget(self.rateWindow, 0, 1)
        layout.addWidget(self.applyButton, 0, 2)
        layout.addWidget(self.exitButton, 1, 2)

        self.setLayout(layout)
        self.setWindowTitle("modyfikuj")
        self.show()