from PyQt5 import Qt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QStandardItem, QFont, QImage


class StandardItem(QStandardItem):
    def __init__(self, txt=None, image_path=None, font_size=12, set_bold=False, color=QColor(0, 0, 0)):
        super().__init__()

        self.fnt = QFont('Open Sans', font_size)
        self.fnt.setBold(set_bold)

        self.setEditable(False)
        self.setForeground(color)
        self.setFont(self.fnt)
        if not txt and not image_path:
            self.setText("Nie dodano jeszcze tej zawartości")
        elif txt:
            self.setText(txt)
        elif image_path:
            image = QImage(image_path)
            smallImage = image.scaled(300, 500, Qt.KeepAspectRatio)
            self.setData(smallImage, Qt.DecorationRole)