from PyQt6 import QtWidgets, uic
import mysql.connector
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import QMessageBox
import os

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sas",
    database="lab_management",
    auth_plugin="mysql_native_password"
)


class LabWorkerWindow(QtWidgets.QMainWindow):
    def __init__(self, user_id, full_name):
        super().__init__()
        uic.loadUi("lab2.ui", self)
        self.setWindowIcon(QIcon("logo.png"))
        self.user_id = user_id
        self.full_name = full_name

        self.label_name.setText(full_name)  # Отображаем ФИО
        self.load_user_photo()  # Загружаем фото

        self.pushButton.clicked.connect(self.logout)  # Кнопка "Выйти"
        self.pushButton_2.clicked.connect(self.add_data)  # Кнопка "Добавить"

    def load_user_photo(self):
        """Загрузка фото исследователя"""
        photo_path = os.path.join(os.getcwd(), "lab1.png")
        if os.path.exists(photo_path):
            pixmap = QPixmap(photo_path)
            self.label_photo.setPixmap(pixmap)
            self.label_photo.setScaledContents(True)

    def add_data(self):
        """Добавление данных через процедуру p2"""
        try:
            name = self.lineEdit.text().strip()
            cost = float(self.lineEdit_2.text().strip())
            code = self.lineEdit_3.text().strip()
            duration = int(self.lineEdit_4.text().strip())
            deviation = float(self.lineEdit_5.text().strip())

            if not name or not code:
                raise ValueError("Название и код не могут быть пустыми")

            cursor = connection.cursor()
            cursor.callproc("p2", (name, cost, code, duration, deviation))
            connection.commit()
            cursor.close()

            QMessageBox.information(self, "Успех", "Данные успешно добавлены!")

            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()
            self.lineEdit_5.clear()
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", f"Некорректный ввод: {str(e)}")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Ошибка БД", f"Ошибка базы данных: {str(e)}")

    def logout(self):
        """Выход и открытие окна входа"""
        self.close()
        from session1 import LoginWindow  # ✅ ОТЛОЖЕННЫЙ ИМПОРТ
        self.login_window = LoginWindow()
        self.login_window.show()
