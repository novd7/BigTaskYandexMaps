import os
import sys

import PyQt5
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.uic.properties import QtGui
from PyQt5.QtCore import Qt


SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self, lat, lon, z=15):
        super().__init__()
        self.lattitude = str(lat)
        self.longtitude = str(lon)
        self.z = z
        self.l = "sat"
        self.getImage()
        self.initUI()

    def getImage(self):
        map_params = {
            "ll": ",".join([self.longtitude, self.lattitude]),
            # "spn": ",".join([self.delta, self.delta]),
            "l": self.l,
            "z": self.z
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        # ... и выполняем запрос
        response = requests.get(map_api_server, params=map_params)

        # Запишем полученное изображение в файл.
        self.map_file = "map.jpg"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        try:
            if event.key() == 16777238:  # pqup
                if not self.z == 17:
                    self.z += 1
            elif event.key() == 16777239:  # pgdown
                if not self.z == 0:
                    self.z -= 1
            elif event.key() == 16777235:  # up
                self.lattitude = str(float(self.lattitude) + 0.005)
            elif event.key() == 16777237:  # down
                self.lattitude = str(float(self.lattitude) - 0.005)
            elif event.key() == 16777234:  # left
                self.longtitude = str(float(self.longtitude) - 0.005)
            elif event.key() == 16777236:  # right
                self.longtitude = str(float(self.longtitude) + 0.005)
            elif event.key() == 77:  # m
                self.l = "map"
            elif event.key() == 83:  # s
                self.l = "sat"
            elif event.key() == 72:  # h
                self.l = "skl"

            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    print("m-схема\ns-спутник\nh-гибрид")
    app = QApplication(sys.argv)
    lattitude = 55.703118
    longtitude = 37.530887
    z = 15
    ex = Example(lattitude, longtitude, z)
    ex.show()
    sys.exit(app.exec())
