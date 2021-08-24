
from PyQt5.QtWidgets import QDateEdit

from PyQt5 import QtCore


from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton


class modifyDataWindow(QWidget):
    path=""
    modifyElementSignal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(modifyDataWindow, self).__init__(parent)
        self.setup()

    def getData(self, data):
        self.path = data


    def sendData(self):
        self.modifyElementSignal.emit(self.dateedit.text().replace('.', '/'))
        self.close()

    def exit(self):
        self.close()

    def setup(self):
        self.releaseDateText = QLabel('Data wydania:', self)
        self.dateedit = QDateEdit(calendarPopup=True)
        self.dateedit.setDateTime(QtCore.QDateTime.currentDateTime())

        self.applyBotton = QPushButton("Zatwierdz", self)
        self.applyBotton.clicked.connect(self.sendData)

        self.exitButton = QPushButton("Anuluj", self)
        self.exitButton.clicked.connect(self.exit)

        layout = QGridLayout()
        layout.addWidget(self.releaseDateText, 0, 0)
        layout.addWidget(self.dateedit, 0, 1)
        layout.addWidget(self.applyBotton, 0, 2)
        layout.addWidget(self.exitButton, 1, 2)

        self.setLayout(layout)
        self.setWindowTitle("modyfikuj")
        self.show()
