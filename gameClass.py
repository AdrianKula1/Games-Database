from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cover = Column(String)
    manufacturer = Column(String)
    releaseDate = Column(String)
    rate = Column(Float)
    comment = Column(String)
    bugs = Column(String)

    def __init__(self, name, cover, releaseDate, manufacturer):
        self.name = name
        self.cover = cover
        self.releaseDate = releaseDate
        self.manufacturer = manufacturer
        self.rate = None
        self.comment = None
        self.bugs = None


# class Game_bugs(Base):
#     __tablename__ = 'games'
#     id = Column(Integer, primary_key=True)
#     gameId = Column(Integer, ForeignKey('clients.id'))
#     text = Column(String)
#
#     game = relationship("Game", back_populates="bugs")
#
#     def __init__(self, gameId, text):
#         self.gameId = gameId
#         self.text = text
