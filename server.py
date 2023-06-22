import os
import pickle
import sys
import threading
import time
from _thread import *
from datetime import date
from socket import *
from typing import NamedTuple

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import gameClass


class messageWindow(QWidget):
    def __init__(self, parent=None):
        super(messageWindow, self).__init__(parent)
        self.showMessage()
        self.server = Server()

    def showMessage(self):
        QMessageBox.information(self, "", "Serwer wystartował. Proszę otworzyć klienta", QMessageBox.Ok)


class GameStruct(NamedTuple):
    name = str
    cover = str
    manufacturer = str
    releaseDate = date
    rate = int
    comment = str
    bugs = str


class Server:
    def __init__(self):
        self.serverThread = threading.Thread(target=self.startServer)
        self.serverThread.start()

    def startServer(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind(('', 8888))
        s.listen(2)

        while 1:
            client, addr = s.accept()
            start_new_thread(self.clientThread, (client,))

    def clientThread(self, client):
        engine = create_engine('sqlite:///database.db', echo=True)
        gameClass.Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        while 1:
            data = pickle.loads(client.recv(4096))
            if data == "refresh":
                result = session.query(gameClass.Game).all()
                for gameToSend in result:
                    time.sleep(0.1)
                    data = pickle.dumps(gameToSend)
                    client.send(data)
            elif data == "add":
                data = client.recv(4096)
                data = pickle.loads(data)
                session.add(data)
                session.commit()
            elif data == "delete":
                gameName = client.recv(4096)
                gameName = pickle.loads(gameName)
                game = session.query(gameClass.Game).filter(gameClass.Game.name.like(gameName)).first()
                if game.cover is not None:
                    os.remove(game.cover)
                session.delete(game)
                session.commit()
            elif data == "modify":
                recvList = client.recv(4096)
                recvList = pickle.loads(recvList)
                game = session.query(gameClass.Game).filter(gameClass.Game.name.like(recvList[1])).first()
                if recvList[0] == "Nazwa":
                    game.name = recvList[2]
                if recvList[0] == "Okładka":
                    game.cover = recvList[2]
                if recvList[0] == "Producent":
                    game.manufacturer = recvList[2]
                elif recvList[0] == "Data wydania":
                    game.releaseDate = recvList[2]
                elif recvList[0] == "Ocena":
                    game.rate = recvList[2]
                elif recvList[0] == "Komentarz":
                    game.comment = recvList[2]
                session.commit()
                # elif gameItem == "Zgłoszone błędy":
                #     game.bugs = modifiedElement
            elif data == "exit":
                break

        client.close()


# engine = create_engine('sqlite:///database.db', echo=True)
#
# gameClass.Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()
# #
# imagePath = os.path.dirname(os.path.realpath(__file__))
# image1path = imagePath + "\images\image1.jpg"
# newGame = gameClass.Game("Life is strange", image1path, "30/01/2015", "DONTNOD")
# session.add(newGame)
# session.commit()
#
# imagePath = os.path.dirname(os.path.realpath(__file__))
# image1path = imagePath + "\images\image2.jpg"
# newGame = gameClass.Game("Wiedźmin 3", image1path, "18/05/2015", "CD Projekt RED")
# session.add(newGame)
# session.commit()


app = QApplication(sys.argv)
mainWindow = messageWindow()
sys.exit(app.exec_())
