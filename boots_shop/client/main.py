import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
import mysql.connector


class Boots(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Корзина покупок обуви")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sas",
            database="boots"
        )
        cursor = db.cursor()
        cursor.execute("call sp_item();")
        result = cursor.fetchall()

        for row in result:
            hbox = QHBoxLayout()

            # Add text QLabel
            data_text = f"Покупатель: {row[0]}, Количество: {row[1]}, Общая цена: {row[2]}\n Сезон: {row[3]}, Товар: {row[4]}, Количество на складе: {row[5]}, Цена товара: {row[6]}\n Дата покупки: {row[7]}\n"
            data_label = QLabel(data_text)
            hbox.addWidget(data_label)

            # Load image from file
            photo_path = row[8]
            photo_pixmap = QPixmap(photo_path)
            photo_label = QLabel()
            photo_label.setPixmap(photo_pixmap)
            hbox.addWidget(photo_label)

            self.layout.addLayout(hbox)

        cursor.close()
        db.close()


if __name__ == "__main__":
    app = QApplication([])
    window = Boots()
    window.show()
    sys.exit(app.exec())
