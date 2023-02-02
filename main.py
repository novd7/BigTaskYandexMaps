import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self, lat, lon, z=15):
        super().__init__()
        self.lattitude = str(lat)
        self.longtitude = str(lon)
        self.z = z
        # self.delta = "0.005"
        self.getImage()
        self.initUI()

    def getImage(self):
        map_params = {
            "ll": ",".join([self.longtitude, self.lattitude]),
            # "spn": ",".join([self.delta, self.delta]),
            "l": "map",
            "z": self.z
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        # ... и выполняем запрос
        response = requests.get(map_api_server, params=map_params)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
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


if __name__ == '__main__':

    app = QApplication(sys.argv)
    lattitude = 55.703118
    longtitude = 37.530887
    z = 15
    ex = Example(lattitude, longtitude, z)
    ex.show()
    sys.exit(app.exec())
