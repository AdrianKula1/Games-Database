import pathlib
import pickle
import sys
import threading
import time
from socket import *

from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTreeView, QAbstractItemView
from sqlalchemy.ext.declarative import declarative_base

import globals
import standardItem
import windows.addGameWindow as addGameWindow
import windows.modifyCommentWindow as modifyCommentWindow
import windows.modifyCoverWindow as modifyCoverWindow
import windows.modifyDateWindow as modifyDateWindow
import windows.modifyManufacturer as modifyManufacturer
import windows.modifyNameWindow as modifyNameWindow
import windows.modifyRateWindow as modifyRateWindow

Base = declarative_base()


class MainWindow(QWidget):
    clicked = ""
    addedGame = []
    itemToDelete = None
    string = None
    gameName, gameItem = None, None

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setup()
        self.clientThread = threading.Thread(target=self.startClient)
        self.clientThread.start()

    def startClient(self):

        s = socket(AF_INET, SOCK_STREAM)
        s.settimeout(4)
        s.connect(('localhost', 8888))
        self.sendRefreshSignal()
        # global gamesCounter
        globals.initialize()
        globals.gamesCounter = 0
        while 1:
            if self.clicked == "refresh":
                s.send(pickle.dumps(self.clicked))
                while 1:
                    try:
                        data = s.recv(4096)
                    except:
                        break
                    globals.gamesCounter += 1
                    data = pickle.loads(data)
                    self.appendGame(data)

                self.clicked = ""
            elif self.clicked == "add":
                s.send(pickle.dumps(self.clicked))
                data = pickle.dumps(self.addedGame)
                s.send(data)
                self.clicked = ""
            elif self.clicked == "delete":
                globals.gamesCounter -= 1
                s.send(pickle.dumps(self.clicked))
                data = pickle.dumps(self.itemToDelete)
                s.send(data)
                self.clicked = ""
            elif self.clicked == "modify":
                s.send(pickle.dumps(self.clicked))
                list = [self.gameItem, self.gameName, self.string]
                s.send(pickle.dumps(list))
                self.clicked = ""
            elif self.clicked == "exit":
                s.send(pickle.dumps(self.clicked))
                self.clicked = ""
                break

        s.close()

    def getData(self, data):
        self.clicked = data

    def appendGame(self, game):
        self.game = standardItem.StandardItem(game.name, '', set_bold=True)
        self.rootNode.appendRow(self.game)

        self.image = standardItem.StandardItem('Okładka', '', set_bold=True)
        self.game.appendRow(self.image)
        self.image_content = standardItem.StandardItem('', game.cover)
        self.image.appendRow(self.image_content)

        self.manufacturer = standardItem.StandardItem('Producent', '', set_bold=True)
        self.game.appendRow(self.manufacturer)
        self.manufacturer_content = standardItem.StandardItem(game.manufacturer)
        self.manufacturer.appendRow(self.manufacturer_content)

        self.releaseDate = standardItem.StandardItem('Data wydania', '', set_bold=True)
        self.game.appendRow(self.releaseDate)
        self.releaseDate_content = standardItem.StandardItem(game.releaseDate)
        self.releaseDate.appendRow(self.releaseDate_content)

        self.rate = standardItem.StandardItem('Ocena', '', set_bold=True)
        self.game.appendRow(self.rate)
        self.rate_content = standardItem.StandardItem((lambda: None, lambda: str(game.rate))[game.rate is not None]())
        self.rate.appendRow(self.rate_content)

        self.comment = standardItem.StandardItem('Komentarz', '', set_bold=True)
        self.game.appendRow(self.comment)
        self.comment_content = standardItem.StandardItem(game.comment)
        self.comment.appendRow(self.comment_content)

        self.bugs = standardItem.StandardItem('Zgłoszone błędy', '', set_bold=True)
        self.game.appendRow(self.bugs)
        self.bugs_content = standardItem.StandardItem(game.bugs)
        self.bugs.appendRow(self.bugs_content)

    def sendRefreshSignal(self):
        self.clicked = "refresh"

    def addGame(self):
        self.addGameWindw = addGameWindow.addGameWindow()
        self.addGameWindw.addGameSignal.connect(self.getGame)

    def getGame(self, data):
        self.addedGame = data
        self.appendGame(self.addedGame)
        self.clicked = "add"
        pass

    def deleteGame(self):

        index = self.gamesWindow.currentIndex()
        if index.row() < 0:
            QMessageBox.information(self, "", "Prosze wybrać grę ktorą chcesz usunąć", QMessageBox.Ok)
            return

        item = self.gamesWindow.selectedIndexes()[0]
        text = item.parent()

        if text.data() is None:
            warningBox = QMessageBox(QMessageBox.Warning, "Uwaga!", "Czy na pewno chcesz usunąć tę grę?",
                                     QMessageBox.Cancel | QMessageBox.Ok, parent=self)
            ret = warningBox.exec()
            if ret == QMessageBox.Ok:
                self.itemToDelete = item.data()
                self.clicked = "delete"
                self.rootNode.removeRow(item.row())

        else:
            QMessageBox.information(self, "", "Prosze wybrać grę a nie jej element", QMessageBox.Ok)

    def modifyElement(self):
        item = self.gamesWindow.selectedIndexes()[0]

        text = item.parent()
        if text.data() == None:
            self.gameItem = "Nazwa"
            self.gameName = item.data()
            self.modifyNameWindow = modifyNameWindow.modifyNameWindow()
            self.modifyNameWindow.setText(item.data())
            self.modifyNameWindow.modifyElementSignal.connect(self.getString)
        else:
            self.gameItem = item.parent().data()
            self.gameName = item.parent().parent().data()
            if item.parent().data() == "Okładka":
                self.coverWindow = modifyCoverWindow.modifyCoverWindow()
                self.destPath = str(pathlib.Path(__file__).parent.absolute())
                self.destPath += "\images\image"
                index = item.parent().parent().row()
                index += 1
                self.destPath += str(index)
                self.destPath += ".jpg"
                self.coverWindow.setText(self.destPath)
                self.coverWindow.modifyElementSignal.connect(self.getString)
            elif item.parent().data() == "Producent":
                self.manufacturerWindow = modifyManufacturer.modifyManufacturerWindow()
                self.manufacturerWindow.setText(item.data())
                self.manufacturerWindow.modifyElementSignal.connect(self.getString)
            elif item.parent().data() == "Data wydania":
                self.dateWindow = modifyDateWindow.modifyDataWindow()
                self.dateWindow.modifyElementSignal.connect(self.getString)
            elif item.parent().data() == "Ocena":
                self.modifyRateWindow = modifyRateWindow.modifyRateWindow()
                self.modifyRateWindow.setText(item.data())
                self.modifyRateWindow.modifyElementSignal.connect(self.getString)
            elif item.parent().data() == "Komentarz":
                self.modifyCommentWindow = modifyCommentWindow.modifyCommentWindow()
                self.modifyCommentWindow.setText(item.data())
                self.modifyCommentWindow.modifyElementSignal.connect(self.getString)
            elif item.parent().data() == "Zgłoszone błędy":
                pass

    def getString(self, data):
        self.string = data
        if self.string.isnumeric():
            if self.string is not None and int(self.string) != -1:
                if self.rootNode.hasChildren():
                    self.rootNode.removeRows(0, self.rootNode.rowCount())
                self.clicked = "modify"
                time.sleep(1)
                self.clicked = "refresh"
                self.string = None
        elif self.string is not None:
            if self.rootNode.hasChildren():
                self.rootNode.removeRows(0, self.rootNode.rowCount())
            self.clicked = "modify"
            time.sleep(1)
            self.clicked = "refresh"
            self.string = None
        else:
            if self.rootNode.hasChildren():
                self.rootNode.removeRows(0, self.rootNode.rowCount())
            self.clicked = "refresh"


    def exit(self):
        self.clicked = "exit"
        self.close()

    def setup(self):
        gamesText = QLabel('Lista gier: ', self)
        self.gamesWindow = QTreeView()
        self.gamesWindow.setMinimumHeight(600)
        self.gamesWindow.setMinimumWidth(900)
        self.gamesWindow.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.gamesWindow.setHeaderHidden(True)
        self.gamesWindow.header().setStretchLastSection(True)

        self.treeModel = QStandardItemModel()
        self.rootNode = self.treeModel.invisibleRootItem()

        self.gamesWindow.setModel(self.treeModel)

        addButton = QPushButton("Dodaj grę", self)
        addButton.clicked.connect(self.addGame)

        deleteButon = QPushButton("Usun gre", self)
        deleteButon.clicked.connect(self.deleteGame)

        modifyButton = QPushButton("Modyfikuj dane", self)
        modifyButton.clicked.connect(self.modifyElement)

        exitButton = QPushButton("Wyjscie", self)
        exitButton.clicked.connect(self.exit)

        layout = QGridLayout()
        layout.setSpacing(6)
        layout.addWidget(gamesText, 0, 0)
        layout.addWidget(self.gamesWindow, 1, 0, 5, 1)
        layout.addWidget(addButton, 1, 1)
        layout.addWidget(deleteButon, 2, 1)
        layout.addWidget(modifyButton, 3, 1)
        layout.addWidget(exitButton, 4, 1)

        self.setLayout(layout)
        self.setWindowTitle("Klient")
        self.show()


app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.setWindowTitle('Client')
mainWindow.setFixedSize(mainWindow.geometry().width(), mainWindow.geometry().height())
mainWindow.move(60, 15)
sys.exit(app.exec_())
