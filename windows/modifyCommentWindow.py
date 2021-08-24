from PyQt5.QtWidgets import QLineEdit
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton

class modifyCommentWindow(QWidget):
    path=""
    modifyElementSignal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(modifyCommentWindow, self).__init__(parent)
        self.setup()

    def setText(self, data):
        if data != "Nie dodano jeszcze tej zawartości":
            self.commentWindow.setText(data)

    def sendData(self):
        self.modifyElementSignal.emit(self.commentWindow.text())
        self.close()


    def exit(self):
        self.close()

    def setup(self):

        self.commentText = QLabel('Komentarz: ', self)
        self.commentWindow = QLineEdit()

        self.applyButton = QPushButton("Zatwierdz", self)
        self.applyButton.clicked.connect(self.sendData)

        self.exitButton = QPushButton("Anuluj", self)
        self.exitButton.clicked.connect(self.exit)

        layout = QGridLayout()
        layout.addWidget(self.commentText, 0, 0)
        layout.addWidget(self.commentWindow, 0, 1)
        layout.addWidget(self.applyButton, 0, 2)
        layout.addWidget(self.exitButton, 1, 2)

        self.setLayout(layout)
        self.setWindowTitle("modyfikuj")
        self.show()